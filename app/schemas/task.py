from typing import Optional

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    name: str = Field(..., example="Название задачи")
    description: Optional[str] = Field(..., example="Описание задачи")


class TaskRead(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Название задачи")
    description: Optional[str] = Field(None, example="Описание задачи")
