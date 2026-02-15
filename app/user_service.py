from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from user_repository import UserRepository
from user_schemas import UserCreate


class UserService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = UserRepository(session)

    def register(self, user: UserCreate):
        # TODO: Проверка на существование пользователч
        result = self.repo.add_one(user.model_dump())
        return result

    def login(): ...

    def logout(): ...

    def get_all_users(self):
        result = self.repo.find_all()
        return result

    def about(self, user_id):
        result = self.repo.find_one(user_id)
        return result

    def update(): ...

    def delete(self, user_id):
        result = self.repo.delete_one(user_id)
        return result


def get_user_service(session: Session = Depends(get_db)):
    return UserService(session)
