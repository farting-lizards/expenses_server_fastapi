from typing import Generator
from pydantic_core import MultiHostUrl
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic import PostgresDsn

DB_URL: PostgresDsn = MultiHostUrl(
    "postgresql://expenses:expenses@localhost:15000/expenses"
)

engine = create_engine(DB_URL.unicode_string(), echo=True)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
