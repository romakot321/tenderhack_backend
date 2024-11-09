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

    async def create_qs(self, auction_url: AuctionUrl) -> QuoteSession:
        id = auction_url.url.rstrip("/").split("/")[-1]
        if not id.isdigit():
            raise HTTPException(HTTPStatus.UNPROCESSABLE_ENTITY)

        url = "https://zakupki.mos.ru/newapi/api/Auction/Get?auctionId=" + str(id)

        auction = await self.req_service.req_to_get_auction(url)
        # TODO: send auction to RabitMQ

        id = auction.id
        return await self.qs_repository.create_or_update_qs(id)

    async def get_qs(self, id: int) -> QuoteSession:
        qs = await self.qs_repository.get_qs(id)
        if qs is None:
            raise HTTPException(HTTPStatus.BAD_REQUEST)
        return qs
