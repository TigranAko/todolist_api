from sqlalchemy import create_engine
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
    DB_URL = "sqlite:///:memory:"
    from sqlalchemy import create_engine, event

    engine = create_engine(
        DB_URL,
        echo=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def enable_sqlite_fk(dbapi_connection, _):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")  # Включаем поддержку FK
        cursor.close()
else:
    DB_URL = "postgresql+psycopg://testuser:testpass@dbps:5432/testdb"

    engine = create_engine(
        DB_URL,
        echo=True,
        pool_pre_ping=True,
    )

Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)


def create_tables():
    Base.metadata.create_all(engine)


def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()
