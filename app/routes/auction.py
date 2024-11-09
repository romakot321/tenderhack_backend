from fastapi import APIRouter, Depends, Response
from app.models.dtos import QuoteSession, AuctionUrl
from app.services.auction import AuctionService

router = APIRouter(prefix='/api/auction', tags=['Auction'])

@router.post("/url", response_model=QuoteSession, status_code=201)
async def post_url(
        response: Response,
        auction_url: AuctionUrl,
        service: AuctionService = Depends()
):
    qs = await service.create_qs(auction_url)
    response.headers["location"] = f"/api/auction/qs/{qs.id}"
    return qs


@router.get("/qs/{id}", status_code=200)
async def get_qs(
        id: int,
        service: AuctionService = Depends()
):
    qs = await service.get_qs(id)
    return qs