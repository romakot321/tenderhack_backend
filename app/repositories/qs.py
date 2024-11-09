from typing import Dict
from app.models.dtos import QuoteSession
from fastapi import HTTPException
from http import HTTPStatus
class QSRepository:
    db = Dict[int, QuoteSession]

    def get_qs(self, id: int) -> QuoteSession:
        return self.db.get(id)
    def create_qs(self, id: int) -> QuoteSession:
        if self.get_qs(id) == None:
            raise HTTPException(status_code=HTTPStatus.CONFLICT)
        self.db[id] = QuoteSession(id=id, status=False)
        qs = self.get_qs(id)
        return qs

