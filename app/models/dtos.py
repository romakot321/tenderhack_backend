from pydantic import BaseModel
from typing import List, Optional, Dict

class AuctionUrl(BaseModel):
    url: str

class QuoteSession(BaseModel):
    status: bool
    reason: str
    warning: bool

class File(BaseModel):
    text: str
    data: List[List[Dict[str, str]]] | None = None
    is_TZ: bool

class Criteries(BaseModel):
    criteries: List[str]

