from getpass import getpass

from expenses_server.db import get_db
from expenses_server.db_models.user import User
from expenses_server import main


def hash_password(password: str) -> str:
    return main.password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return main.password_context.verify(plain_password, hashed_password)


def create_user(username: str) -> None:
    password = getpass()
    password_hash = main.password_context.hash(password)
    user = User(username=username, password_hash=password_hash)
    session = next(get_db())
    session.add(user)
    session.commit()
