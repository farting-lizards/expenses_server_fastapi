from typing import TYPE_CHECKING
from uuid import uuid4
from sqlalchemy import Integer, String
from sqlalchemy.orm import MappedColumn as Column, Mapped
from .core import Base
from sqlalchemy.orm import relationship


if TYPE_CHECKING:
    from .expense import Expense


class Account(Base):
    __tablename__ = "accounts"
    name: Mapped[str] = Column(String, unique=True)
    expenses: Mapped["Expense"] = relationship("Expense", back_populates="account")
    id: Mapped[int] = Column(Integer, primary_key=True, default=uuid4)
