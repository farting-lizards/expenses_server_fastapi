from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from expenses_server.dtos.users import UserToken
from expenses_server.settings import settings
from expenses_server.db import get_db
from expenses_server.db_models.user import User
from expenses_server.security import create_access_token
from expenses_server.utils import verify_password
from expenses_server.security import oauth2_scheme

router = APIRouter(prefix="/users")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db_session: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.jwt_encode_key, algorithms=[settings.jwt_algorithm]
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    try:
        user = (
            db_session.query(User)
            .where(
                User.username == username,
            )
            .one()
        )
    except NoResultFound:
        raise credentials_exception
    return user


@router.get("/me", response_model=User)  # TODO: No need to send password_hash
async def read_user_current(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    # TODO: Only accounts for user should be sent
    return current_user


@router.post("/token")
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
        access_token = create_access_token(data={"sub": user.username})
        return UserToken(access_token=access_token, token_type="bearer")
    except NoResultFound:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect username or password"
        )
