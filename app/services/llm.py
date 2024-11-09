import asyncio
import uuid

from loguru import logger
from aio_pika import DeliveryMode, ExchangeType, Message, connect
from aio_pika.abc import AbstractIncomingMessage



class LLMService:
    exchange_out_name = "requests"
    exchange_in_name = "responses"

    async def consume(self, queue):
        while True:
            await asyncio.sleep(1)
            msg = await queue.get(timeout=5, fail=False)
            if not msg:
                continue
            logger.debug(msg.body.decode())
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

    async def publish(self, text: str):
        logger.debug("Start connecting publish")
        connection = await connect("amqp://guest:guest@localhost/")
        async with connection:
            logger.debug("Connected publish")
            channel = await connection.channel()
            exchange = await channel.declare_exchange(
                self.exchange_out_name, ExchangeType.DIRECT,
            )
            logger.debug("Declared publish")

            message = Message(
                text.encode(),
                delivery_mode=DeliveryMode.PERSISTENT,
            )
            logger.debug("Formed message publish")

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
