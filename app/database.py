from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy

#DB_URL = "sqlite+aiosqlite:///database2.db"
# DB_URL = "sqlite:///database2.db"
DB_URL = "postgresql+psycopg://testuser:testpass@dbps:5432/testdb"

engine = create_engine(
        DB_URL,
        echo=True,
        #        connect_args={"check_same_thread": False}  # Только для SQLite
        )

Session = sessionmaker(autoflush=False, autocommit=False , bind=engine)

#Base = declarative_base()
class Base(DeclarativeBase):
    pass

def create_tables():
    Base.metadata.create_all(engine)

def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()
#    with Session() as session:
#        yield session

