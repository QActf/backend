from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = "QActf"
    description: str = "QActf"
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "SECRET"
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    lifetime_seconds = 3600
    max_password_length = 3
    max_length_string = 100
    min_length_string = 1
    full_amount_minimum = 0

    rows = 100
    columns = 3

    class Config:
        env_file = ".env"


settings = Settings()
