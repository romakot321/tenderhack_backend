from app.models.dtos import QuoteSession

db = dict[int, QuoteSession]()


class QSRepository:
    async def get_qs(self, id: int) -> QuoteSession:
        print("Get", db, id)
        return db.get(id)

    async def create_or_update_qs(self, id: int) -> QuoteSession:
        db[id] = QuoteSession(id=id, status=False, reason="", warning=False)
        qs = await self.get_qs(id)
        print("Create or update", db, qs)
        return qs

    async def update_qs(self, qs: QuoteSession):
        db[qs.id] = qs
        print("Update", db, qs)

