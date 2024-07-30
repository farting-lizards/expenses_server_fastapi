from fastapi import APIRouter, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext


from .settings import settings

from .routes.accounts import router as account_router
from .routes.expenses import router as expense_router
from .routes.users import router as user_router

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()


@app.get("/")
async def root() -> FileResponse:
    response = FileResponse(f"{settings.frontend_path}/index.html")
    return response


base_router = APIRouter(prefix="/api")


base_router.include_router(account_router)
base_router.include_router(expense_router)
base_router.include_router(user_router)

app.include_router(base_router)


if settings.frontend_path is not None:
    app.mount("/", StaticFiles(directory=settings.frontend_path), name="static")
