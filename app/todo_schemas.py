from datetime import datetime

from pydantic import BaseModel


class ToDo(BaseModel):
    id: int
    user_id: int | None = None
    title: str
    description: str
    completed: bool = False
    created_at: datetime = datetime.now()
    completed_at: datetime | None = None
