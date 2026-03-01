from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import Base


class SQLAlchemyRepository:
    model: Base
    # TODO: replace commit to UoF

    def __init__(self, session: AsyncSession):
        self.db: AsyncSession = session

    async def add_one(self, entity):
        stmt = insert(self.model).values(**entity).returning(self.model.id)
        result = await self.db.execute(stmt)
        answer = result.scalar_one_or_none()
        await self.db.commit()
        return answer

    async def find_all(self):
        stmt = select(self.model)  # TODO: Добавить фильтрацию и пагинацию и сортировку
        result = await self.db.execute(stmt)
        answer = result.scalars().all()
        return answer

    async def find_one(self, entity_id):
        stmt = select(self.model).where(self.model.id == entity_id)
        result = await self.db.execute(stmt)
        answer = result.scalar_one_or_none()
        return answer

    async def edit_one(self, entity_id, entity):
        stmt = (
            update(self.model)
            .where(self.model.id == entity_id)
            .values(**entity)
            .returning(self.model.id)
        )
        result = await self.db.execute(stmt)
        answer = result.scalar_one_or_none()
        await self.db.commit()
        return answer

    async def delete_one(self, entity_id):
        stmt = (
            delete(self.model)
            .where(self.model.id == entity_id)
            .returning(self.model.id)
        )
        result = await self.db.execute(stmt)
        answer = result.scalar_one_or_none()
        await self.db.commit()
        return answer
