from getpass import getpass
import hashlib

from expenses_server.db import get_db
from expenses_server.db_models.user import User
from expenses_server.settings import settings


def create_user(username: str) -> None:
    algorithm = "sha256"
    password = getpass()
    m = hashlib.sha256()
    m.update((settings.password_seed + password).encode("utf8"))
    password_hash = f"{algorithm}:{m.hexdigest()}"
    user = User(username=username, password_hash=password_hash)
    session = next(get_db())
    session.add(user)
    session.commit()
