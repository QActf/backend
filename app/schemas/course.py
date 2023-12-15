from typing import Optional

from pydantic import BaseModel


class CourseCreate(BaseModel):
    name: str
    description: Optional[str]


class CourseRead(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True
