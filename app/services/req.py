from app.models.aucton import Auction
from requests import request
from http import HTTPMethod
from fastapi import HTTPException
from http import HTTPStatus


class RequestService:
    async def req_to_get_auction(self, url: str) -> Auction:
        resp = request(HTTPMethod.GET, url=url, timeout=3)
        json_data = resp.json()
        auction = None
        try:
            auction = Auction.model_validate(json_data)
        except ValueError as e:
            raise HTTPException(HTTPStatus.BAD_REQUEST)
        return auction
