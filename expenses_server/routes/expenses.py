from uuid import UUID
from fastapi import APIRouter, Depends
from pydantic import UUID4

from ..db import get_db
from ..db_models.category import Category
from ..dtos.expenses import ExpenseDTO, ExpenseCreate, ExpenseUpdate
from ..db_models.expense import Expense as DBExpense
from sqlalchemy.orm import Session


router = APIRouter(prefix="/expenses")


@router.post("", response_model=ExpenseDTO)
async def create_expense(
    expense: ExpenseCreate, session: Session = Depends(get_db)
) -> DBExpense:
    db_category = (
        session.query(Category).filter(Category.name == expense.category_name).first()
    )
    db_expense = DBExpense(
        amount=expense.amount,
        description=expense.description,
        currency=expense.currency.value,
        # TODO Default category should be handled better
        # TODO Should the default not be set for category?
        category_id=db_category.id if db_category is not None else 13,
        account_id=expense.account_id,
    )
    session.add(db_expense)
    session.commit()
    session.refresh(db_expense)
    return db_expense


@router.get("", response_model=list[ExpenseDTO])
async def get_all_expenses(session: Session = Depends(get_db)) -> list[ExpenseDTO]:
    db_expenses = session.query(DBExpense).all()
    expenses = [ExpenseDTO.model_validate(expense) for expense in db_expenses]
    return expenses


@router.patch("/{expense_id}", response_model=ExpenseDTO)
async def update_expense(
    expense_id: UUID4, expense_update: ExpenseUpdate, session: Session = Depends(get_db)
) -> ExpenseDTO:
    session.query(DBExpense).filter(DBExpense.id == expense_id).update(
        values=expense_update.model_dump(exclude_none=True)  # type: ignore
    )
    session.commit()
    updated_expense = session.get(DBExpense, expense_id)
    return ExpenseDTO.model_validate(updated_expense)
