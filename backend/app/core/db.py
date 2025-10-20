from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import SQLITE_URL

engine = create_engine(
    SQLITE_URL,
    connect_args={"check_same_thread": False},
    future=True
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, future=True)
Base = declarative_base()

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cur = dbapi_connection.cursor()
    cur.execute("PRAGMA foreign_keys=ON")
    cur.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
