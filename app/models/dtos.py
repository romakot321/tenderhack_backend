from pydantic import BaseModel
from typing import List, Optional, Dict

class AuctionSchema(BaseModel):
    url: str
    criteries: Optional[List[str]]

class QuoteSession(BaseModel):
    id: int
    status: bool
    reason: str
    warning: bool

class File(BaseModel):
    text: str
    data: Optional[List[List[Dict[str, str]]]]
    is_TZ: bool

