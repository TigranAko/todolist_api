from typing import Annotated

from fastapi import APIRouter, Depends, Path

from schemas import UserCreate
from user_service import UserService, get_user_service

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/all")
async def get_users_info(service: UserService = Depends(get_user_service)):
    # service = get_user_service()
    users = service.get_all_users()
    return {
        "users": users,
    }


@router.post("/register")  # , response_model=UserReturn)
async def register(user: UserCreate, service: UserService = Depends(get_user_service)):
    service.register(user)
    return {"message": "User registered successfully!"}


@router.get("/user/{user_id}")
async def get_user_info(
    user_id: Annotated[int, Path()], service: UserService = Depends(get_user_service)
):
    user = service.about(user_id)
    return user


@router.delete("/user/{user_id}")
async def delete_user_info(
    user_id: Annotated[int, Path()], service: UserService = Depends(get_user_service)
):
    # ADD AUTO DELETING TODOS
    user_id = service.delete(user_id)
    return {"message": "user deleted with tasks", "user_id": user_id}
