from fastapi import Depends, HTTPException
from app.repositories.qs import QSRepository
from app.models.dtos import AuctionUrl, QuoteSession
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

    async def create_qs(self, auction_url: AuctionUrl):
        # TODO: get data of auction and send it to RabitMQ
        auction = await self.req_service.req_to_get_auction(auction_url)
        print(auction)

        id = auction_url.url.split()[-1]
        if id.isdigit() != True:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
        id = int(id)
        return self.qs_repository.create_qs(id)

    async def get_qs(self, id: int) -> QuoteSession:
        return self.qs_repository.get_qs(id)

