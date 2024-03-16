from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..db_models.account import Account as DBAccount
from ..dtos.accounts import Account


router = APIRouter(prefix="/accounts")


@router.get("", response_model=list[Account])
def get_all_accounts(db: Session = Depends(get_db)) -> list[DBAccount]:
    # TODO: Only accounts for user should be sent
    return db.query(DBAccount).all()
