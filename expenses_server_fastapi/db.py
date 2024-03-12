from pydantic_core import MultiHostUrl
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import PostgresDsn

DB_URL: PostgresDsn = MultiHostUrl(
    "postgresql://expenses:expenses@localhost:15000/expenses"
)

engine = create_engine(DB_URL.unicode_string(), echo=True)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
