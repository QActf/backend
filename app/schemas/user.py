from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, WithJsonSchema, field_serializer
from sqlalchemy_utils import Choice
from typing_extensions import Annotated

from app.core.constants import Role


class RoleMixin:
    role: Annotated[Choice, WithJsonSchema({'type': 'str'})]

    @field_serializer('role')
    def serialize_role(self, role: Choice, _info):
        return role.code


class UserReadRegister(schemas.BaseUser[int]):
    username: str
    tariff_id: Optional[int]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserRead(RoleMixin, UserReadRegister):
    pass


class UserList(RoleMixin, BaseModel):
    id: int
    email: str
    username: str

    class Config:
        arbitrary_types_allowed = True


class UserCreate(schemas.BaseUserCreate):
    role: Role
    username: str


class UserUpdate(schemas.BaseUserUpdate):
    role: Optional[Role]
    username: Optional[str]


class UserChangePassword(schemas.BaseUserUpdate):
    password: str


class UserTariffUpdate(schemas.BaseUserUpdate):
    tariff_id: int


class UserTariffDelete(schemas.BaseUserUpdate):
    tariff_id: None
