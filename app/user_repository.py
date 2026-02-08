from sqlalchemy import select

from .base_repository import SQLAlchemyRepository
from .models import UserBase


class UserRepository(SQLAlchemyRepository):
    model = UserBase

    def find_password(self, username):
        stmt = select(self.model.password).where(self.model.username == username)
        result = self.db.execute(stmt)
        answer = result.scalar_one_or_none()
        return answer
