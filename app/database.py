from app.config import config_db
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)
from sqlalchemy.pool import StaticPool

url_to_db = config_db.db_url

if config_db.ENVIROMENT in {"TEST", "DEV"}:
    from sqlalchemy import event

    engine = create_async_engine(
        url_to_db,
        echo=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine.sync_engine, "connect")
    def enable_sqlite_fk(dbapi_connection, _):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")  # Включаем поддержку FK
        cursor.close()
else:
    # "postgresql+psycopg://testuser:testpass@dbps:5432/testdb"
    engine = create_async_engine(
        url_to_db,
        pool_pre_ping=True,
    )

LocalAsyncSession = async_sessionmaker(autoflush=False, autocommit=False, bind=engine)


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)


async def close_connection_pool():
    await engine.dispose()
