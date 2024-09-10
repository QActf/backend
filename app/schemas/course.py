from typing import Optional

from pydantic import BaseModel, Field, validator

from app.schemas.task import TaskRead


class CourseCreate(BaseModel):
    name: str
    description: Optional[str]


class CourseRead(BaseModel):
    id: int
    name: str = Field(serialization_alias='title')
    description: Optional[str] = Field(serialization_alias='subtitle')
    in_development: Optional[bool]
    is_closed: Optional[bool]
    icon: Optional[str]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class CourseTasksRead(CourseRead):
    tasks: Optional[list[TaskRead]]


class MultiCourseForUserRead(BaseModel):
    id: int
    name: str = Field(serialization_alias='title')
    description: str = Field(serialization_alias='subtitle')
    status: str
    icon: Optional[str]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class CourseTariffCreate(BaseModel):
    course_id: int
    tariff_id: int


class CourseUpdate(BaseModel):
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    in_development: Optional[bool] = Field(None)
    icon: Optional[str] = Field(None)

    @validator('name')
    def name_cannot_be_null(cls, value):
        """Проверка, есть ли название у курса."""
        if value is None or not value.strip():
            raise ValueError('Название курса не может быть пустым.')
        return value
