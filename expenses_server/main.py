from http import HTTPStatus
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session

from expenses_server.db_models.user import User
from expenses_server.dtos.users import UserToken
from expenses_server.utils import hash_password, verify_password

from .settings import settings

from .routes.accounts import router as account_router
from .routes.expenses import router as expense_router
from .routes.users import router as user_router
from expenses_server.db import get_db
from sqlalchemy.exc import NoResultFound

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()


@app.get("/")
async def root() -> FileResponse:
    response = FileResponse(f"{settings.frontend_path}/index.html")
    return response


@app.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: Session = Depends(get_db),
) -> UserToken:
    try:
        user = (
            db_session.query(User)
            .where(
                User.username == form_data.username,
            )
            .one()
        )
        if not verify_password(form_data.password, user.password_hash):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Incorrect username or password",
            )
        return UserToken(access_token=user.username, token_type="bearer")
    except NoResultFound:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect username or password"
        )


base_router = APIRouter(prefix="/api")


base_router.include_router(account_router)
base_router.include_router(expense_router)
base_router.include_router(user_router)

app.include_router(base_router)


if settings.frontend_path is not None:
    app.mount("/", StaticFiles(directory=settings.frontend_path), name="static")
