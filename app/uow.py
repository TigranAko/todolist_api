from app.database import LocalAsyncSession
from app.todo_repository import TodoRepository
from app.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork:
    def __init__(self):
        self.async_session_factory = LocalAsyncSession

    async def __aenter__(self):
        self.session: AsyncSession = self.async_session_factory()

        # TODO: При добавлении репозитория класс не должен изменяться
        # нарушение принципа sOlid
        self.users = UserRepository(self.session)
        self.todos = TodoRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.close()


async def get_uow() -> UnitOfWork:
    async with UnitOfWork() as uow:
        yield uow
