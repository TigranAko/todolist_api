from app.base_repository import SQLAlchemyRepository
from app.models import ToDoBase
from sqlalchemy import select


class TodoRepository(SQLAlchemyRepository):
    model = ToDoBase

    async def find_user_todos(self, user_id):
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = await self.db.execute(stmt)
        answer = result.scalars().all()
        return answer
