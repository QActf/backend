from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "QActf"
    description: str = "QActf"
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "SECRET"
    first_superuser_email: Optional[str] = None
    first_superuser_password: Optional[str] = None

    lifetime_seconds: int = 3000
    max_password_length: int = 3
    max_length_string: int = 100
    min_length_string: int = 1
    media_url: str = 'media/'
    base_dir: Path = Path(__file__).parent.parent.parent

    class Config:
        env_file = "infra/.env"


settings = Settings()
