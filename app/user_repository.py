from sqlalchemy import select

from base_repository import SQLAlchemyRepository
from models import UserBase


class UserRepository(SQLAlchemyRepository):
    model = UserBase

    async def find_password(self, username):
        stmt = select(self.model.password).where(self.model.username == username)
        result = await self.db.execute(stmt)
        answer = result.scalar_one_or_none()
        return answer

    async def is_have_username(self, username) -> bool:
        stmt = select(True).where(self.model.username == username)
        result = await self.db.execute(stmt)
        answer = result.scalar_one_or_none()
        return answer
