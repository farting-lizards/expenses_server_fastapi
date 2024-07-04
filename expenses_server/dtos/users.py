from typing import Annotated
from uuid import uuid4
from fastapi import Depends
from pydantic import UUID4, BaseModel

from ..security import oauth2_scheme


class User(BaseModel):
    id: UUID4
    username: str


class UserToken(BaseModel):
    access_token: str
    token_type: str


def fake_decode_token(token: str) -> User:
    return User(id=uuid4(), username=f"{token} fakedecoded")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    user = fake_decode_token(token)
    return user
