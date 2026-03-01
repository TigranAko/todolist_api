from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from user_repository import UserRepository
from user_schemas import UserCreate


class UserService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = UserRepository(session)

    async def register(self, user: UserCreate):
        if self.repo.is_have_username(user.username):
            # TODO: change status code
            # TODO: split app exceptions and http exceptions
            raise HTTPException(
                400, detail="Пользователь с таким именем уже существует"
            )
        result = self.repo.add_one(user.model_dump())
        return result

    async def login(): ...

    async def logout(): ...

    async def get_all_users(self):
        result = self.repo.find_all()
        return result

    async def about(self, user_id):
        result = self.repo.find_one(user_id)
        return result

    async def update(): ...

    async def delete(self, user_id):
        result = self.repo.delete_one(user_id)
        return result


async def get_user_service(session: Session = Depends(get_db)):
    return UserService(session)
