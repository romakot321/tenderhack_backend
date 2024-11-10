from pydantic import BaseModel
from typing import List, Optional, Dict


class AuctionSchema(BaseModel):
    url: str
    criteria: list[str]


class QuoteSession(BaseModel):
    id: int
    status: bool
    reason: str
    warning: bool


class File(BaseModel):
    path: str
    is_TZ: bool

