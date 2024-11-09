from fastapi import Depends, HTTPException
from app.repositories.qs import QSRepository
from app.models.dtos import AuctionSchema, QuoteSession, Criterion
from http import HTTPStatus
from .req import RequestService


class AuctionService:
    def __init__(
            self,
            qs_repository: QSRepository = Depends(),
            req_service: RequestService = Depends()

    ):
        self.qs_repository = qs_repository
        self.req_service = req_service

    async def create_qs(self, auction_schema: AuctionSchema) -> QuoteSession:
        id = auction_schema.url.rstrip("/").split("/")[-1]
        if not id.isdigit():
            raise HTTPException(HTTPStatus.UNPROCESSABLE_ENTITY)

        url = "https://zakupki.mos.ru/newapi/api/Auction/Get?auctionId=" + str(id)

        auction = await self.req_service.req_to_get_auction(url)

        for val in Criterion:
            match val:
                case "name": # Проверить имя на соответствие
                    break
                case "executor":
                    if auction.isContractGuaranteeRequired: # Требуется обеспечение исполнения контракта
                        pass
                    break
                case "license":
                    if len(auction.licenseFiles) > 0: # Требуется проверить наличие сертификатов/лицензий
                        pass
                    break
                case "delivery_schedule":
                    if len(auction.deliveries) > 0: # Требуется проверить на соответствие даты, место и товары
                        pass
                    break
                case "max_cost":
                    if auction.contractCost is not None: # Требуется проверить максимальную цену контракта
                        pass
                    break
                case "start_cost":
                    if auction.startCost is not None: # Должно быть значение "Цена контракта"
                        pass
                    break
                case "task_document": # Проверить auction.deliveries.items на соответствие
                    break

        # TODO: send auction to RabitMQ

        id = auction.id
        return await self.qs_repository.create_or_update_qs(id)

    async def get_qs(self, id: int) -> QuoteSession:
        qs = await self.qs_repository.get_qs(id)
        if qs is None:
            raise HTTPException(HTTPStatus.BAD_REQUEST)
        return qs
