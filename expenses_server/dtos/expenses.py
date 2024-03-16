from datetime import datetime
from pydantic import UUID4, BaseModel

from .accounts import Account
from .categories import CategoryEnum


class ExpenseBase(BaseModel):
    amount: float
    currency: CategoryEnum  # TODO: In OpenApI this does not show option "EUR"
    description: str | None
    category_name: str = "other"
    account_id: int


class ExpenseCreate(ExpenseBase):
    class Config:
        form_attributes = True


class Expense(BaseModel):
    id: UUID4
    timestamp: datetime
    account: Account
    amount: float
    currency: CategoryEnum
    description: str | None

    class Config:
        form_attributes = True
