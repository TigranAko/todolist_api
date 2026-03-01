from fastapi import Depends

from uow import UnitOfWork, get_uow


class TodoService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_all_todos(self):
        """Список всех задач (для админа)"""
        result = await self.uow.todos.find_all()
        return result

    async def get_user_todos(self, user_id: int):
        """Список задач пользователя"""
        result = await self.uow.todos.find_user_todos(user_id)
        return result

    async def get_todo(self, todo_id: int):
        """Получить задачу"""
        result = await self.uow.todos.find_one(todo_id)
        return result

    async def create_todo(self, todo):
        """Создать задачу"""
        result = await self.uow.todos.add_one(todo.model_dump())
        return result

    async def create_todos(self, todos):
        """Создать задачи"""
        # TODO: need optimization
        result = []
        for todo in todos:
            await result.append(await self.uow.todos.add_one(todo.model_dump()))
        return result

    async def update_todo(self, todo_id, todo):
        """Создать задачу"""
        result = await self.uow.todos.edit_one(todo_id, todo)
        return result

    async def delete_todo(self, todo_id):
        """Создать задачу"""
        result = await self.uow.todos.delete_one(todo_id)
        return result


async def get_todo_service(uow: UnitOfWork = Depends(get_uow)):
    return TodoService(uow)
