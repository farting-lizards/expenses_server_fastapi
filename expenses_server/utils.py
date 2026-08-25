from getpass import getpass

import bcrypt

from expenses_server.db import get_db
from expenses_server.db_models.user import User


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def create_user(username: str) -> None:
    password = getpass()
    user = User(username=username, password_hash=hash_password(password))
    session = next(get_db())
    session.add(user)
    session.commit()
