import datetime
from typing import Optional

from pydantic import (
    BaseModel, Field, WithJsonSchema, field_serializer, field_validator,
)
from sqlalchemy_utils import Choice
from typing_extensions import Annotated

from app.core.constants import Gender


class ProfileRead(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    second_name: Optional[str]
    birthday: Optional[datetime.date]
    gender: Optional[
        Annotated[
            Choice,
            WithJsonSchema({'type': 'str'})
        ]
    ]
    user_id: int
    image: Optional[str]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @field_serializer('gender')
    def serialize_gender(self, gender: Choice, _info):
        return gender.code


class ProfileUpdate(BaseModel):
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    second_name: Optional[str] = Field(None)
    birthday: Optional[datetime.date] = Field(None)
    gender: Optional[str] = Field(None)

    @field_validator('gender')
    @classmethod
    def check_gender(cls, v: str):
        genders = [gender.value for gender in Gender]
        if v not in genders:
            raise ValueError(f'В поле гендер может быть только: {genders}')
        return v


class ProfileCreate(ProfileUpdate):
    user_id: int
