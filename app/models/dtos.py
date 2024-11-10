from pydantic import BaseModel
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
    criteria: list[Criterion]


class QuoteSession(BaseModel):
    id: int
    status: bool
    reason: str
    warning: bool


class File(BaseModel):
    path: str
    is_TZ: bool

