from pydantic import BaseModel


class CourseRead(BaseModel):
    name: str
    description: str


class CourseCreate(CourseRead):
    pass
