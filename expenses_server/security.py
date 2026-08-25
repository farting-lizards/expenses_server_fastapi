from http import HTTPStatus
from typing import Annotated, Any
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from expenses_server.db import get_db
from expenses_server.db_models.user import User
from expenses_server.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/token")


def create_access_token(
    data: dict[str, Any],  # TODO: Make data's type def more strict
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_encode_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


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
