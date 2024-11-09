from app.models.dtos import QuoteSession
class QSRepository:
    db = dict[int, QuoteSession]()

    async def get_qs(self, id: int) -> QuoteSession:
        return self.db.get(id)
    async def create_or_update_qs(self, id: int) -> QuoteSession:
        self.db[id] = QuoteSession(id=id, status=False, reason="", warning=False)
        qs = await self.get_qs(id)
        return qs

    async def update_qs(self, qs: QuoteSession) :
        self.db[qs.id] = qs
        return

