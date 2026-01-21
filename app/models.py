from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class UserBase(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(), unique=True)
    password: Mapped[str] = mapped_column(String())
    tasks: Mapped[list["ToDoBase"]] = relationship(
        "ToDoBase",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class ToDoBase(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["UserBase"] = relationship("UserBase", back_populates="tasks")
    title: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    completed: Mapped[bool] = mapped_column(Boolean(), default=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
