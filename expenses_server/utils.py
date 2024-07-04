from getpass import getpass
import hashlib

from expenses_server.db import get_db
from expenses_server.db_models.user import User
from expenses_server.settings import settings


def hash_password(password: str) -> str:
    # TODO: Rename m
    m = hashlib.sha256()  # TODO: This should be consistent with settings.hash_algorithm
    m.update((settings.password_seed + password).encode("utf8"))
    return f"{settings.hash_algorithm}:{m.hexdigest()}"


def create_user(username: str) -> None:
    password = getpass()
    password_hash = hash_password(password)
    user = User(username=username, password_hash=password_hash)
    session = next(get_db())
    session.add(user)
    session.commit()
