from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from database import create_tables
from todo_router import router as todo_router
from user_router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(todo_router)


if __name__ == "__main__":
    uvicorn.run("main:app")
    # uvicorn.run("main:app", host="0.0.0.0", port=80)
