from fastapi import Depends, HTTPException

from uow import UnitOfWork, get_uow
from user_schemas import UserCreate


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def register(self, user: UserCreate):
        if await self.uow.users.is_have_username(user.username):
            # TODO: change status code
            # TODO: split app exceptions and http exceptions
            raise HTTPException(
                400, detail="Пользователь с таким именем уже существует"
            )
        result = await self.uow.users.add_one(user.model_dump())
        return result

    async def login(): ...

    async def logout(): ...

    async def get_all_users(self):
        result = await self.uow.users.find_all()
        return result

    async def about(self, user_id):
        result = await self.uow.users.find_one(user_id)
        return result

    async def update(): ...

    async def delete(self, user_id):
        result = await self.uow.users.delete_one(user_id)
        # TODO: Можно удалять задачи вручную
        return result


async def get_user_service(uow: UnitOfWork = Depends(get_uow)):
    return UserService(uow)
