from sqlalchemy import select

from base_repository import SQLAlchemyRepository
from models import ToDoBase


class TodoRepository(SQLAlchemyRepository):
    model = ToDoBase

    def find_user_todos(self, user_id):
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = self.db.execute(stmt)
        answer = result.scalars().all()
        return answer
