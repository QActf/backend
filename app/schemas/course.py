from typing import Optional

from pydantic import BaseModel, Field, validator

from app.schemas.task import TaskRead


class CourseCreate(BaseModel):
    name: str
    description: Optional[str]


class CourseRead(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True


class CourseTasksRead(CourseRead):
    tasks: Optional[list[TaskRead]]


class MultiCourseRead(BaseModel):
    id: int
    name: str
    description: str
    is_available: bool
    is_started: bool

    class Config:
        from_attributes = True


class CourseTariffCreate(BaseModel):
    course_id: int
    tariff_id: int


class CourseUpdate(BaseModel):
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)

    @validator('name')
    def name_cannot_be_null(cls, value):
        """Проверка, есть ли название у курса."""
        if value is None or not value.strip():
            raise ValueError('Название курса не может быть пустым.')
        return value
