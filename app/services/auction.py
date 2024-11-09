from fastapi import Depends, HTTPException
from app.repositories.qs import QSRepository
from app.models.dtos import AuctionUrl
from http import HTTPStatus
class AuctionService:
    def __init__(
            self,
            qs_repository: QSRepository = Depends()
    ):
        self.qs_repository = qs_repository

    async def create_qs(self, auction_url: AuctionUrl):
        # TODO: get data of auction and send it to RabitMQ

        id = auction_url.url.split()[-1]
        if id.isdigit() != True:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
        id = int(id)
        return self.qs_repository.create_qs(id)
