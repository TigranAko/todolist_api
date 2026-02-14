from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from todo_repository import TodoRepository


class TodoService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = TodoRepository(session)

    def get_all_todos(self):
        """Список всех задач (для админа)"""
        result = self.repo.find_all()
        return result

    def get_user_todos(self, user_id: int):
        """Список задач пользователя"""
        result = self.repo.find_user_todos(user_id)
        return result

    def get_todo(self, todo_id: int):
        """Получить задачу"""
        result = self.repo.find_one(todo_id)
        return result

    def create_todo(self, todo):
        """Создать задачу"""
        result = self.repo.add_one(todo.model_dump())
        return result

    def create_todos(self, todos):
        """Создать задачи"""
        # TODO: need optimization
        result = []
        for todo in todos:
            result.append(self.repo.add_one(todo.model_dump()))
        return result

    def update_todo(self, todo_id, todo):
        """Создать задачу"""
        result = self.repo.edit_one(todo_id, todo)
        return result

    def delete_todo(self, todo_id):
        """Создать задачу"""
        result = self.repo.delete_one(todo_id)
        return result


def get_todo_service(session: Session = Depends(get_db)):
    return TodoService(session)
