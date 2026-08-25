import os

from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.environ.get("ENV_FILE", ".env"))

    db_url: PostgresDsn = MultiHostUrl(
        "postgresql://expenses:expenses@localhost:15000/expenses"
    )
    frontend_path: str | None = None  # "../expenses-react/build"

    jwt_encode_key: str
    jwt_algorithm: str = "HS256"
    jwt_token_expire_minutes: int = 1440  # 24 hours


settings = Settings()
