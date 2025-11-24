from datetime import datetime
from typing import Annotated

from fastapi import Query
from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class UserCreate(User):
    pass


class UserReturn(User):
    id: int


class ToDo(BaseModel):
    id: int
    user_id: int | None = None
    title: str
    description: str
    completed: bool = False
    created_at: datetime = datetime.now()
    completed_at: datetime | None = None


class Pagination(BaseModel):
    limit: Annotated[
        int,
        Query(10, le=100, title="Количество элементов на 1 странице", alias="count"),
    ]
    offset: Annotated[int, Query(0, title="Смещение", alias=["start"])]
    sort_by: Annotated[str, Query("id", title="Сортировка", alias=["sort"])]


class Filtration(BaseModel):
    completed: Annotated[bool | None, Query(None)]
    created_after: Annotated[datetime | None, Query(None)]
    created_before: Annotated[datetime | None, Query(None)]
    completed_after: Annotated[datetime | None, Query(None)]
    completed_before: Annotated[datetime | None, Query(None)]
    title_contains: Annotated[str | None, Query(None)]
