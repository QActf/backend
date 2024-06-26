from typing import Optional

from fastapi_users import schemas
from pydantic import WithJsonSchema, field_serializer
from sqlalchemy_utils import Choice
from typing_extensions import Annotated

from app.core.constants import Role


class UserRead(schemas.BaseUser[int]):
    role: Annotated[
        Choice,
        WithJsonSchema({'type': 'str'})
    ]
    username: str
    tariff_id: Optional[int]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @field_serializer('role')
    def serialize_role(self, role: Choice, _info):
        return role.code


class UserCreate(schemas.BaseUserCreate):
    role: Role
    username: str


class UserUpdate(schemas.BaseUserUpdate):
    role: Optional[Role]
    username: Optional[str]
