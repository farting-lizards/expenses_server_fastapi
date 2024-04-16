from curses.panel import update_panels
from http import HTTPStatus
from typing import cast
from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4

from expenses_server.dtos.currencies import CurrencyEnum

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
    db_expenses = session.query(DBExpense).order_by(DBExpense.timestamp.desc()).all()
    expenses = [ExpenseDTO.model_validate(expense) for expense in db_expenses]
    return expenses


@router.get("/{expense_id}", response_model=ExpenseDTO)
async def get_expense(
    expense_id: UUID4, session: Session = Depends(get_db)
) -> ExpenseDTO:
    db_expense = session.get(DBExpense, expense_id)
    if db_expense is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Expense with id {expense_id} not found",
        )
    return ExpenseDTO.model_validate(db_expense)


@router.patch("/{expense_id}", response_model=ExpenseDTO)
async def update_expense(
    expense_id: UUID4, expense_update: ExpenseUpdate, session: Session = Depends(get_db)
) -> ExpenseDTO:
    # TODO: Ask David - How to best refactor this
    payload = expense_update.model_dump(exclude_none=True)

    # Replace category_name with category_id
    if payload.get("category_name") is not None:
        db_category = (
            session.query(Category)
            .filter(Category.name == payload.get("category_name", "other"))
            .first()
        )
        del payload["category_name"]
        payload["category_id"] = db_category.id if db_category is not None else 13
    # Replace currency name with currency
    if payload.get("currency"):
        payload["currency"] = cast(CurrencyEnum, payload["currency"]).value

    session.query(DBExpense).filter(DBExpense.id == expense_id).update(
        values=payload  # type: ignore
    )
    session.commit()
    updated_expense = session.get(DBExpense, expense_id)
    return ExpenseDTO.model_validate(updated_expense)


@router.delete("/{expense_id}", response_model=ExpenseDTO)
async def delete_expenses(
    expense_id: UUID4, db: Session = Depends(get_db)
) -> ExpenseDTO:
    db_expense = db.get(DBExpense, expense_id)
    if db_expense is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Expense with id {expense_id} not found",
        )

    expense = ExpenseDTO.model_validate(db_expense)
    db.delete(db_expense)
    db.commit()
    return expense
