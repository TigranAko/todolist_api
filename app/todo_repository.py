from .base_repository import SQLAlchemyRepository
from .models import ToDoBase


class UserRepository(SQLAlchemyRepository):
    model = ToDoBase
