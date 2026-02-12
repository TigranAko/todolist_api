from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session

from database import Base


class SQLAlchemyRepository:
    model: Base
    # TODO: replace commit to UoF

    def __init__(self, session: Session):
        self.db: Session = session

    def add_one(self, entity):
        stmt = insert(self.model).values(**entity).returning(self.model.id)
        result = self.db.execute(stmt)
        answer = result.scalar_one_or_none()
        self.db.commit()
        return answer

    def find_all(self):
        stmt = select(self.model)  # TODO: Добавить фильтрацию и пагинацию и сортировку
        result = self.db.execute(stmt)
        answer = result.scalars().all()
        return answer

    def find_one(self, entity_id):
        stmt = select(self.model).where(self.model.id == entity_id)
        result = self.db.execute(stmt)
        answer = result.scalar_one_or_none()
        return answer

    def edit_one(self, entity_id, entity):
        stmt = (
            update(self.model)
            .where(self.model.id == entity_id)
            .values(**entity)
            .returning(self.model.id)
        )
        result = self.db.execute(stmt)
        answer = result.scalar_one_or_none()
        self.db.commit()
        return answer

    def delete_one(self, entity_id):
        stmt = (
            delete(self.model)
            .where(self.model.id == entity_id)
            .returning(self.model.id)
        )
        result = self.db.execute(stmt)
        answer = result.scalar_one_or_none()
        self.db.commit()
        return answer
