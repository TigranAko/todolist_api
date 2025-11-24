from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

# class Base(DeclarativeBase):
#    pass
"""
class Parent(Base):
    __tablename__ = "parent"
    id = mapped_column(Integer, primary_key=True)
    children = relationship(
        "Child", back_populates="parent", cascade="all, delete", passive_deletes=True,
    ) [2](https://docs.sqlalchemy.org/en/20/orm/cascades.html)

class Child(Base):
    __tablename__ = "child"
    id = mapped_column(Integer, primary_key=True)
    parent_id = mapped_column(Integer, ForeignKey("parent.id", ondelete="CASCADE"))
    parent = relationship("Parent", back_populates="children")
"""


class UserBase(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String())
    password: Mapped[str] = mapped_column(String())
    tasks: Mapped[list["ToDoBase"]] = relationship(
        back_populates="user"
    )  # , cascade="all, delete-orphan")


class ToDoBase(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    #    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    #    user_id: Mapped[int] = ForeignKey("users.id", ondelete="CASCADE"
    user: Mapped["UserBase"] = relationship(
        back_populates="tasks"
    )  # "users.id", ondelete="CASCADE"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    title: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    completed: Mapped[bool] = mapped_column(Boolean())

    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=None, nullable=True
    )
