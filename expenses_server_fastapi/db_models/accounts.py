from uuid import uuid4
from sqlalchemy import UUID, Column, String
from expenses_server_fastapi.db import Base


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String, unique=True)