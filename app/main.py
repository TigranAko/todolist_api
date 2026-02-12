from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, Path, Query

from crud import (
    create_todo,
    delete_todo,
    get_todo,
    get_todos,
    update_todo,
    update_todo_completed,
)
from database import create_tables, get_db
from schemas import Filtration, Pagination, ToDo
from user_router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)


@app.get("/todos")
async def get_todos_info(
    pagination: Annotated[Pagination, Query] = Depends(),
    filtration: Annotated[Filtration, Query] = Depends(),
    db=Depends(get_db),
):
    result = get_todos(filtration, pagination, db)
    return {"tasks": result}


@app.post("/todo")
async def add_todo(todo: ToDo, db=Depends(get_db)):
    create_todo(todo, db)
    return {"message": "ToDo created successfully!"}


@app.post("/todos")
async def creates_todos(todos: list[ToDo], db=Depends(get_db)):
    for todo in todos:
        create_todo(todo, db)
    return {"message": "ToDos created successfully!"}


@app.put("/todo/{todo_id}")
async def update_todo_info(
    todo_id: Annotated[int, Path()], todo: ToDo, db=Depends(get_db)
):
    return update_todo(todo_id, todo, db)


@app.patch("/todo")
async def update_todos_completed(
    ids: Annotated[str, Path()], completed: Annotated[bool, Path()]
):
    ids = ids.split(",")
    for todo_id in ids:
        update_todo_completed(todo_id, completed)
    return {"Данные обновлены"}


@app.get("/todo/{todo_id}")
async def get_todo_info(todo_id: Annotated[int, Path()], db=Depends(get_db)):
    return get_todo(todo_id, db).one()


@app.delete("/todo/{todo_id}")
async def delete_todo_info(todo_id: Annotated[int, Path()], db=Depends(get_db)):
    delete_todo(todo_id, db)
    return {"message": "todo (task) deleted"}


if __name__ == "__main__":
    uvicorn.run("main:app")
    # uvicorn.run("main:app", host="0.0.0.0", port=80)
