import asyncio
import uuid
import json
from fastapi import Depends
from loguru import logger
from aio_pika import DeliveryMode, ExchangeType, Message, connect
from aio_pika.abc import AbstractIncomingMessage

from app.repositories.qs import QSRepository
from app.models.dtos import QuoteSession
from app.models.llm import LLMParametersSchema
from app.services import _llm_cache


class LLMService:
    exchange_out_name = "requests"
    exchange_in_name = "responses"

    def __init__(self, qs_repository: QSRepository = Depends()):
        self.qs_repository = qs_repository

    def _parse_answer(self, qs_id: int, text: str) -> QuoteSession:
        return QuoteSession(
            id=qs_id,
            status=True,
            reason=text,
            warning=False
        )

    async def consume(self, queue):
        while True:
            await asyncio.sleep(1)

            msg = await queue.get(timeout=5, fail=False)
            if not msg:
                continue

            body = json.loads(msg.body.decode())
            qs = self._parse_answer(body["id"], body["text"])
            self._set_cache_analyze(body["id"], qs)
            await self.qs_repository.update_qs(qs)

            await msg.ack()

    async def connect(self):
        connection = await connect("amqp://guest:guest@localhost/")
        async with connection:
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=1)

            exchange = await channel.declare_exchange(
                self.exchange_in_name, ExchangeType.DIRECT,
            )
            queue = await channel.declare_queue(
                'llmresponses', durable=True, exclusive=False, auto_delete=False
            )

            await queue.bind(exchange, routing_key='out')
            logger.info("Start rabbit consuming")
            task = asyncio.create_task(self.consume(queue))
            await asyncio.gather(task)

    def _get_cached_analyze(self, qs_id: int) -> QuoteSession | None:
        logger.debug("Get from cache " + str(qs_id) + str(_llm_cache.get(qs_id)))
        return _llm_cache.get(qs_id)

    def _set_cache_analyze(self, qs_id: int, qs: QuoteSession):
        logger.debug("Set to cache " + str(qs_id) + str(qs))
        _llm_cache[qs_id] = qs

    async def publish(self, params: LLMParametersSchema):
        cached = self._get_cached_analyze(params.qs_id)
        if cached is not None:
            return await self.qs_repository.update_qs(cached)

        connection = await connect("amqp://guest:guest@localhost/")
        async with connection:
            channel = await connection.channel()
            exchange = await channel.declare_exchange(
                self.exchange_out_name, ExchangeType.DIRECT,
            )

            message = Message(
                params.model_dump_json().encode(),
                delivery_mode=DeliveryMode.PERSISTENT,
            )

            await exchange.publish(message, routing_key="in")
            logger.debug(f"Sent {message!r}")


async def on_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        logger.debug(f"Received {message.body.decode()}")


if __name__ == "__main__":
    async def main():
        service = LLMService()
        await service.connect()
        await service.publish(str(uuid.uuid4()))
        while True:
            await asyncio.sleep(5)

    asyncio.run(main())
