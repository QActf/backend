from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import EmailStr


class Settings(BaseSettings):
    app_title: str = "QActf"
    description: str = "QActf"
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "SECRET"
    first_superuser_email: Optional[str] = None
    first_superuser_password: Optional[str] = None

    lifetime_seconds: int = 3600
    max_password_length: int = 3
    max_length_string: int = 100
    min_length_string: int = 1

    class Config:
        env_file = ".env"


settings = Settings()
