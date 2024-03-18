from uuid import uuid4, UUID
from sqlalchemy import (
    TIMESTAMP,
    ForeignKey,
    Text,
    func,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .core import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .category import Category
    from .account import Account


class Expense(Base):
    __tablename__ = "expenses"

    # TODO: Restrict type of currency
    currency: Mapped[str]
    amount: Mapped[float] = mapped_column()
    description: Mapped[str | None] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(
        "Category", back_populates="expenses", init=False
    )

    # TODO: Check if back_populates and corresponding value in account is needed
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    account: Mapped["Account"] = relationship(
        "Account", back_populates="expenses", init=False
    )

    external_id: Mapped[str | None] = mapped_column(unique=True, default=None)
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    timestamp: Mapped[str] = mapped_column(
        TIMESTAMP, nullable=False, default=func.now()
    )
