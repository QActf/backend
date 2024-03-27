from enum import Enum
from typing import Optional

from fastapi_users import schemas
from pydantic import Field


class Role(str, Enum):
    user = "user"
    manager = "manager"
    admin = "admin"


class UserRead(schemas.BaseUser[int]):
    role: Role
    username: str = Field(..., example="Имя")
    tariff_id: Optional[int]

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    role: Role
    username: str = Field(..., example="Имя")


class UserUpdate(schemas.BaseUserUpdate):
    role: Optional[Role]
    username: Optional[str] = Field(..., example="Имя")
