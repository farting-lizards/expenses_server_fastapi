from fastapi import APIRouter, FastAPI

from .routes.accounts import router as account_router
from .routes.expenses import router as expense_router
from sqlalchemy import event
from .db_models.account import Account
from .db_models.category import Category
from .seed_db import populate_accounts, populate_categories


app = FastAPI()
base_router = APIRouter(prefix="/api")


event.listen(Category.__table__, "after_create", populate_categories)
event.listen(Account.__table__, "after_create", populate_accounts)


base_router.get("/")


async def root() -> dict[str, str]:
    return {"message": "Hello World"}


base_router.include_router(account_router)
base_router.include_router(expense_router)

app.include_router(base_router)
