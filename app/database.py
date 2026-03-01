from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
)
from sqlalchemy.pool import StaticPool

test = True  # TODO: use .env file
if test:
    # DB_URL = "sqlite+aiosqlite:///database2.db"
    # DB_URL = "sqlite:///database2.db"
    DB_URL = "sqlite+aiosqlite:///:memory:"
    from sqlalchemy import event

    engine = create_async_engine(
        DB_URL,
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
    DB_URL = "postgresql+psycopg://testuser:testpass@dbps:5432/testdb"

    engine = create_async_engine(
        DB_URL,
        echo=True,
        pool_pre_ping=True,
    )

Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
LocalAsyncSession = async_sessionmaker(autoflush=False, autocommit=False, bind=engine)


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)


async def create_tables():
    async with engine.connect() as connection:
        await connection.run_sync(Base.metadata.create_all)
        await connection.commit()
        await connection.aclose()


async def close_connection_pool():
    await engine.dispose()


async def get_db():
    session: AsyncSession = LocalAsyncSession()
    try:
        yield session
    finally:
        await session.aclose()
