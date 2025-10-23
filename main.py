from fastapi import FastAPI, Depends, HTTPException, status,Query, Path
from typing import Annotated

from .schemas import ToDo, User, UserCreate, UserReturn, Pagination, Filtration

from contextlib import asynccontextmanager
from .database import get_db, create_tables
from .crud import get_users, get_todos, create_user, create_todo, delete_user, get_user, delete_todo, get_todo, update_todo, update_todo_completed



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def get_users_info(db = Depends(get_db)):
    users = get_users(db)
    return {
            "users": users,
            }


@app.post("/register")#, response_model=UserReturn)
async def register(user: UserCreate, db = Depends(get_db)):
    create_user(user, db)
    return {"message": "User registered successfully!"}


@app.get("/user/{user_id}")
async def get_user_info(user_id: Annotated[int, Path()], db = Depends(get_db)):
    user = get_user(user_id, db)
    return user


@app.delete("/user/{user_id}")
async def delete_user_info(user_id: Annotated[int, Path()], db = Depends(get_db)):
    # ADD AUTO DELETING TODOS
    delete_user(user_id, db)
    return {"message": "user deleted with tasks"}


@app.get("/todos")
async def get_todos_info(
        pagination: Annotated[Pagination, Query] = Depends(),
        filtration: Annotated[Filtration, Query] = Depends(),
        db = Depends(get_db)
        ):
    result = get_todos(filtration, pagination, db)
    return {"tasks": result}

@app.post("/todo")
async def add_todo(
        todo: ToDo,
        db = Depends(get_db)
    ):
    create_todo(todo, db)
    return {"message": "ToDo created successfully!"}


@app.post("/todos")
async def creates_todos(todos: list[ToDo], db = Depends(get_db)):
    for todo in todos:
        create_todo(todo, db)
    return {"message": "ToDos created successfully!"}


@app.put("/todo/{todo_id}")
async def update_todo_info(todo_id: Annotated[int, Path()], todo: ToDo, db = Depends(get_db)):
    return update_todo(todo_id, todo, db)


@app.patch("/todo")
async def update_todos_completed(ids: Annoteated[str, Path()], completed: Annotated[bool, Path()]):
    ids = ids.split(',')
    for todo_id in ids:
        update_todo_completed(todo_id, completed)
    return {"Данные обновлены"}



@app.get("/todo/{todo_id}")
async def get_todo_info(
        todo_id: Annotated[int, Path()],
        db = Depends(get_db)
    ):
    return get_todo(todo_id, db).one()


@app.delete("/todo/{todo_id}")
async def delete_todo_info(todo_id: Annotated[int, Path()], db = Depends(get_db)):
    delete_todo(todo_id , db)
    return {"message": "todo (task) deleted"}
