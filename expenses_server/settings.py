import os

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Later files win
    model_config = SettingsConfigDict(
        env_file=os.environ.get("ENV_FILE", (".env.dev", ".env"))
    )

    db_url: PostgresDsn = PostgresDsn(
        "postgresql://expenses:expenses@localhost:15000/expenses"
    )
    frontend_path: str | None = None  # "../expenses-react/build"

    jwt_encode_key: str
    jwt_algorithm: str = "HS256"
    jwt_token_expire_minutes: int = 1440  # 24 hours


# jwt_encode_key comes from the env file, which mypy can't see
settings = Settings()  # type: ignore[call-arg]
