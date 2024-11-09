from app.models.dtos import AuctionUrl
from app.models.aucton import Auction
from requests import request
from http import HTTPMethod
class RequestService:

    async def req_to_get_auction(self, auction_url: AuctionUrl) -> Auction:
        resp = request(HTTPMethod.GET, url=auction_url.url, timeout=3)
        json_data = resp.json()
        auction = None
        try:
            auction = Auction.model_validate(json_data)
        except ValueError as e:
            print("Error parsing response data:", e)
        return auction
