from sqlalchemy.ext.asyncio import AsyncSession

from database import LocalAsyncSession
from todo_repository import TodoRepository
from user_repository import UserRepository


class UnitOfWork:
    def __init__(self):
        self.async_session_factory = LocalAsyncSession

    async def __aenter__(self):
        self.session: AsyncSession = self.async_session_factory()

        # TODO: При добавлении репозитория класс не должен изменяться
        # нарушение принципа sOlid
        self.users = UserRepository(self.async_session_factory)
        self.todos = TodoRepository(self.async_session_factory)

        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.close()
