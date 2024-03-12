from uuid import uuid4
from sqlalchemy import TIMESTAMP, UUID, Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from expenses_server_fastapi.db import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(UUID, primary_key=True, default=uuid4)
    external_id = Column(String, unique=True)
    amount = Column(Float, nullable=False)
    # TODO: Restrict type of currency
    currency = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    description = Column(Text)

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("category", back_populates="expenses")

    # TODO: Check if back_populates and corresponding value in account is needed
    account_id = Column(Integer, ForeignKey("accounts.id"))
    account = relationship("account", back_populates="expenses")
