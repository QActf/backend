from typing import Optional

from pydantic import (
    BaseModel, Field, WithJsonSchema, field_serializer, field_validator,
    validator,
)
from sqlalchemy_utils import Choice
from typing_extensions import Annotated

from app.core.constants import StatusCourse
from app.schemas.task import TaskRead


class CourseCreate(BaseModel):
    name: str
    description: Optional[str]


class CourseRead(BaseModel):
    id: int
    name: Optional[str] = Field(serialization_alias='title')
    description: Optional[str] = Field(serialization_alias='subtitle')
    icon: Optional[str]
    status: Optional[
        Annotated[
            Choice,
            WithJsonSchema({'type': 'str'})
        ]
    ]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @field_serializer('status')
    def serialize_gender(self, status: Choice, _info):
        return status.code


class CourseTasksRead(CourseRead):
    tasks: Optional[list[TaskRead]]


class MultiCourseRead(BaseModel):
    id: int
    name: str = Field(serialization_alias='title')
    description: str = Field(serialization_alias='subtitle')
    is_available: bool
    is_started: bool
    icon: Optional[str]
    status: Optional[
        Annotated[
            Choice,
            WithJsonSchema({'type': 'str'})
        ]
    ]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class CourseTariffCreate(BaseModel):
    course_id: int
    tariff_id: int


class CourseUpdate(BaseModel):
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    icon: Optional[str] = Field(None)
    status: Optional[str] = Field(None)

    @validator('name')
    def name_cannot_be_null(cls, value):
        """Проверка, есть ли название у курса."""
        if value is None or not value.strip():
            raise ValueError('Название курса не может быть пустым.')
        return value

    @field_validator('status')
    @classmethod
    def check_status(cls, v: str):
        status = [status.value for status in StatusCourse]
        if v not in status:
            raise ValueError(f'В поле "status" может быть только: {status}')
        return v
