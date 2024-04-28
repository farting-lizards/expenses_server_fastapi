from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: PostgresDsn = MultiHostUrl(
        "postgresql://expenses:expenses@localhost:15000/expenses"
    )


settings = Settings()
