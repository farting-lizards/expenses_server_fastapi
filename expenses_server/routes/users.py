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
