from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: PostgresDsn = MultiHostUrl(
        "postgresql://expenses:expenses@localhost:15000/expenses"
    )
    frontend_path: str | None = None  # "../expenses-react/build"

    # Password
    hash_algorithm: str = "sha256"
    password_seed: str = "dummy_seed"

    jwt_encode_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # TODO: Generate correctly
    jwt_algorithm: str = "HS256"
    jwt_token_expire_minutes: int = 1  # TODO: Longer expiration time


settings = Settings()
