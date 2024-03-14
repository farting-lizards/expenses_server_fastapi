from fastapi import FastAPI
from expenses_server_fastapi.db import Base, engine
from .routes.accounts import router as account_router
from .routes.expenses import router as expense_router
from sqlalchemy import event
from expenses_server_fastapi.db_models.account import Account
from expenses_server_fastapi.db_models.category import Category
from expenses_server_fastapi.seed_db import populate_accounts, populate_categories

app = FastAPI()


event.listen(Category.__table__, "after_create", populate_categories)
event.listen(Account.__table__, "after_create", populate_accounts)

Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(account_router)
app.include_router(expense_router)
