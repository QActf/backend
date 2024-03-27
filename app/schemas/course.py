from typing import Optional

from pydantic import BaseModel, Field, validator


class CourseCreate(BaseModel):
    name: str = Field(..., example="Название курса")
    description: Optional[str] = Field(..., example="Описание курса")


class CourseRead(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True


class CourseUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Название курса")
    description: Optional[str] = Field(None, example="Описание курса")

    @validator('name')
    def name_cannot_be_null(cls, value):
        """Проверка, есть ли название у курса."""
        if value is None or not value.strip():
            raise ValueError('Название курса не может быть пустым.')
        return value
