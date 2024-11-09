from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import StrEnum

class Criterion(StrEnum):
    NAME = "name"
    EXECUTOR = "executor"
    LICENCE = "license"
    DELIVERY_SCHEDULE = "delivery_schedule"
    MAX_COST = "max_cost"
    START_COST = "start_cost"
    TASK_DOCUMENT = "task_document"
class AuctionSchema(BaseModel):
    url: str
    criteria: Optional[List[Criterion]]

class QuoteSession(BaseModel):
    id: int
    status: bool
    reason: str
    warning: bool

class File(BaseModel):
    text: str
    data: List[List[Dict[str, str]]] | None = None
    is_TZ: bool

