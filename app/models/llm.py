from pydantic import BaseModel

from app.models.dtos import File


class LLMParametersSchema(BaseModel):
    qs_id: int
    criteria: list[str]
    files: list[File]

