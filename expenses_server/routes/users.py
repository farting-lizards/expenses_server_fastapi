from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from expenses_server.dtos.users import UserDTO, UserToken
from expenses_server.db import get_db
from expenses_server.db_models.user import User
from expenses_server.security import create_access_token, get_current_user
from expenses_server.utils import verify_password

router = APIRouter(prefix="/users")


@router.get("/me", response_model=UserDTO)
async def read_user_current(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserDTO:
    return UserDTO.model_validate(current_user)


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
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user.username})
        return UserToken(access_token=access_token, token_type="bearer")
    except NoResultFound:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
