from fastapi import APIRouter, FastAPI

from .routes.accounts import router as account_router
from .routes.expenses import router as expense_router


app = FastAPI()
base_router = APIRouter(prefix="/api")


base_router.get("/")


async def root() -> dict[str, str]:
    return {"message": "Hello World"}


base_router.include_router(account_router)
base_router.include_router(expense_router)

app.include_router(base_router)
