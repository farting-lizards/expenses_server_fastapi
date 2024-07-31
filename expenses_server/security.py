from typing import Any
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
import jwt

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
