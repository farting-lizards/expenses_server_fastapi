from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from expenses_server.db import get_db
from expenses_server.db_models.user import User
from expenses_server.dtos.users import UserToken, get_current_user
from expenses_server.utils import hash_password


router = APIRouter(prefix="/users")


@router.get("/me", response_model=list[User])
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
                User.password_hash == hash_password(form_data.password),
            )
            .one()
        )
        return UserToken(access_token=user.username, token_type="bearer")
    except NoResultFound as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect username or password"
        )
