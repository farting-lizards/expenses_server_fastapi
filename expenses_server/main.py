from fastapi import FastAPI
from .db import engine
from .db_models.core import Base
from .routes.accounts import router as account_router
from .routes.expenses import router as expense_router
from sqlalchemy import event
from .db_models.account import Account
from .db_models.category import Category
from .seed_db import populate_accounts, populate_categories

app = FastAPI()


event.listen(Category.__table__, "after_create", populate_categories)
event.listen(Account.__table__, "after_create", populate_accounts)

Base.metadata.create_all(bind=engine)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


app.include_router(account_router)
app.include_router(expense_router)
