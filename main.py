from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.database import close_connection_pool
from app.todo_router import router as todo_router
from app.user_router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_connection_pool()


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(todo_router)


if __name__ == "__main__":
    uvicorn.run("main:app")
    # uvicorn.run("main:app", host="0.0.0.0", port=80)
