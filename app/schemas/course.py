from typing import Optional

from pydantic import BaseModel, Field


class CourseCreate(BaseModel):
    name: str
    description: Optional[str]


class CourseRead(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True


class CourseUpdate(BaseModel):
    name: Optional[str] = Field(None,)
    description: Optional[str] = Field(None,)
