from datetime import datetime
from typing import Annotated
from pydantic import UUID4, BaseModel, Field, computed_field, field_serializer
from .categories import Category
from .accounts import Account
from .currencies import CurrencyEnum


class ExpenseBase(BaseModel):
    amount: float
    currency: CurrencyEnum  # TODO: In OpenApI this does not show option "EUR"
    description: str | None
    category_name: str = "other"
    account_id: int


class ExpenseCreate(ExpenseBase):
    class Config:
        from_attributes = True


class ExpenseUpdate(BaseModel):
    amount: float | None = None
    currency: CurrencyEnum | None = None
    description: str | None = None
    category_name: str | None = None
    account_id: int | None = None


class ExpenseDTO(BaseModel):
    id: UUID4
    timestamp: datetime
    account: Account
    amount: float
    currency: CurrencyEnum
    description: str | None
    category: Category

    @field_serializer("category")
    def serialize_category(self, category: Category) -> str:
        return category.name

    class Config:
        from_attributes = True
