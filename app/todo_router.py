from typing import Annotated

from fastapi import APIRouter, Depends, Path

from schemas import ToDo
from todo_service import TodoService, get_todo_service

router = APIRouter(prefix="/todo", tags=["ToDo"])


@router.get("/all")
async def get_todos_info(
    # pagination: Annotated[Pagination, Query] = Depends(),
    # filtration: Annotated[Filtration, Query] = Depends(),
    service: TodoService = Depends(get_todo_service),
):
    # result = get_todos(filtration, pagination, db)
    result = service.get_all_todos()
    return {"tasks": result}


@router.put("/{todo_id}")
async def get_my_todos(
    user_id: Annotated[int, Path()],
    service: TodoService = Depends(get_todo_service),
):
    # TODO: user_id должен определяться сам
    return service.get_user_todos(user_id)


@router.put("/{todo_id}")
async def get_user_todos(
    user_id: Annotated[int, Path()],
    service: TodoService = Depends(get_todo_service),
):
    return service.get_user_todos(user_id)


@router.post("/create")
async def add_todo(
    todo: ToDo,
    service: TodoService = Depends(get_todo_service),
):
    service.create_todo(todo)
    return {"message": "ToDo created successfully!"}


@router.post("/create_todos")
async def creates_todos(
    todos: list[ToDo],
    service: TodoService = Depends(get_todo_service),
):
    for todo in todos:
        service.create_todo(todo)
    return {"message": "ToDos created successfully!"}


@router.put("/{todo_id}")
async def update_todo_info(
    todo_id: Annotated[int, Path()],
    todo: ToDo,
    service: TodoService = Depends(get_todo_service),
):
    # TODO: Не работает
    return service.update_todo(todo_id, todo)


"""
@router.patch("/")
async def update_todos_completed(
    ids: Annotated[str, Path()],
    completed: Annotated[bool, Path()],
    service: TodoService = Depends(get_todo_service),
):
    ids = ids.split(",")
    for todo_id in ids:
        service.update_todo_completed(todo_id, completed)
    return {"Данные обновлены"}
"""


@router.get("/{todo_id}")
async def get_todo_info(
    todo_id: Annotated[int, Path()],
    service: TodoService = Depends(get_todo_service),
):
    return service.get_todo(todo_id)


@router.delete("/{todo_id}")
async def delete_todo_info(
    todo_id: Annotated[int, Path()],
    service: TodoService = Depends(get_todo_service),
):
    service.delete_todo(todo_id)
    return {"message": "todo (task) deleted"}
