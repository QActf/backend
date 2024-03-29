from typing import Optional

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    name: str
    description: Optional[str]


class TaskRead(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
