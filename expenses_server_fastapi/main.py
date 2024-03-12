from typing import Any
from fastapi import FastAPI
from expenses_server_fastapi.db import Base, engine
from expenses_server_fastapi.db_models.expense import Expense
from .routes.accounts import router as account_router
from sqlalchemy import event, Connection, Table
from expenses_server_fastapi.db_models.account import Account
from expenses_server_fastapi.db_models.category import Category
from expenses_server_fastapi.seed_db import populate_accounts, populate_categories

app = FastAPI()


def expense_created(target: Table, connection: Connection, **ke: Any):
    print("UAUAUAUAUUAUAUAUAUAU_______________________________-")


event.listen(Category.__table__, "after_create", populate_categories)
event.listen(Account.__table__, "after_create", populate_accounts)

Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(account_router)
