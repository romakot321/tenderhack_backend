from fastapi import Depends, HTTPException
from http import HTTPStatus

from app.repositories.qs import QSRepository
from app.repositories.file import FileRepository
from app.models.dtos import AuctionSchema, QuoteSession
from app.models.llm import LLMParametersSchema
from app.services.req import RequestService
from app.services.llm import LLMService


class AuctionService:
    get_auction_url = "https://zakupki.mos.ru/newapi/api/Auction/Get?auctionId="

    def __init__(
            self,
            qs_repository: QSRepository = Depends(),
            req_service: RequestService = Depends(),
            llm_service: LLMService = Depends(),
            file_repository: FileRepository = Depends()
    ):
        self.qs_repository = qs_repository
        self.req_service = req_service
        self.llm_service = llm_service
        self.file_repository = file_repository

    async def create_qs(self, auction_schema: AuctionSchema) -> QuoteSession:
        id = auction_schema.url.rstrip("/").split("/")[-1]
        if not id.isdigit():
            raise HTTPException(HTTPStatus.UNPROCESSABLE_ENTITY)

        auction = await self.req_service.req_to_get_auction(self.get_auction_url + str(id))
        qs = await self.qs_repository.create_or_update_qs(auction.id)
        qs_files = []
        for file in auction.files:
            qs_files.append(self.file_repository.handle_file(file.id))
        params = LLMParametersSchema(qs_id=auction.id, criteria=auction_schema.criteria, files=qs_files)
        await self.llm_service.publish(params)

        return qs

    async def get_qs(self, id: int) -> QuoteSession:
        qs = await self.qs_repository.get_qs(id)
        if qs is None:
            raise HTTPException(404)
        return qs
