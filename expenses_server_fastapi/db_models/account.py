from uuid import uuid4
from sqlalchemy import Column, Integer, String
from expenses_server_fastapi.db import Base
from sqlalchemy.orm import relationship


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, default=uuid4)
    name = Column(String, unique=True)
    expenses = relationship("Expense", back_populates="account")
