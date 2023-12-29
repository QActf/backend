from enum import Enum
from typing import Optional

from fastapi_users import schemas


class Role(str, Enum):
    user = "user"
    manager = "manager"
    admin = "admin"


class UserRead(schemas.BaseUser[int]):
    role: Role
    username: str
    tariff_id: Optional[int]

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    role: Role
    username: str


class UserUpdate(schemas.BaseUserUpdate):
    role: Optional[Role]
    username: Optional[str]
