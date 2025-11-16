from sqlalchemy.orm import Session
from models import UserBase, ToDoBase
from schemas import User, ToDo, Pagination, Filtration
from sqlalchemy import text


def get_users(db: Session):
    return db.query(UserBase).all()


def get_todos(filtration: Filtration, pagination: Pagination, db: Session):
    result = db.query(ToDoBase)
    if filtration:
        if filtration.completed is not None:
#            result = result.filter(ToDoBase.completed == True)
            result = result.where(ToDoBase.completed == True)
            if filtration.completed == True:
                if filtration.completed_after:
                    result = result.where(ToDoBase.complated_at < filtration.completed_after)
                if filtration.completed_before:
                    result = result.where(ToDoBase.complated_at > filtration.completed_after)

        if filtration.created_after:
            result = result.where(ToDoBase.created_at < filtration.created_after)
        if filtration.created_before:
            result = result.where(ToDoBase.created_at > filtration.created_after)

        if filtration.title_contains:
            result = result.where(ToDoBase.title.ilike(f"%{filtration.title_contains}%"))

    if pagination:
        sort_field = pagination.sort_by
        if sort_field.startswith('-'):
            sort_field = getattr(ToDoBase, sort_field[1:], ToDoBase.id).desc()
        else:
            sort_field = getattr(ToDoBase, sort_field, ToDoBase.id)


        result = db.query(ToDoBase).order_by(
                #pagination.sort_by if not pagination.sort_by.startswith('-') else desc(pagination.sort_by[1:])
                sort_field
                ).offset(pagination.offset).limit(pagination.limit)
    return result.all()


def get_user(user_id, db: Session):
    return db.query(UserBase).filter(UserBase.id == user_id).one()


def create_user(user: User, db: Session):
    user_db = UserBase(**user.model_dump())
    db.add(user_db)
    db.commit()


def delete_user(user_id: int, db: Session):
    db.query(UserBase).filter(UserBase.id == user_id).delete()
    #db.query(ToDoBase).filter(ToDoBase.user_id == user_id).delete() # удаление должно быть из бд
    db.commit()


def create_todo(todo: ToDo, db: Session):
    todo_db = ToDoBase(**todo.model_dump())
    db.add(todo_db)
    db.commit()


def update_todo(todo_id, todo: ToDo, db: Session):
    db.query(ToDoBase).filter(ToDoBase.id == todo_id).update({
        ToDoBase.user_id: todo.user_id,
        ToDoBase.title: todo.title,
        ToDoBase.description: todo.description,
        ToDoBase.completed: todo.completed
        })
    db.commit()

def update_todo_completed(todo_id, completed: bool, db: Session):
    todo = get_todo(todo_id, db)
    todo.update({ToDoBase.completed: completed})
    db.commit()
    db.refresh()


def get_todo(todo_id, db: Session):
    return db.query(ToDoBase).where(ToDoBase.id == todo_id)


def delete_todo(todo_id: int, db: Session):
    db.query(ToDoBase).filter(ToDoBase.id == todo_id).delete()
    db.commit()
