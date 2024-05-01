from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: PostgresDsn = MultiHostUrl(
        "postgresql://expenses:expenses@localhost:15000/expenses"
    )
    frontend_path: str | None = None  # "../expenses-react/build"


settings = Settings()
