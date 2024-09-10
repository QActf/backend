from typing import Optional

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    name: str
    description: Optional[str]
    difficult: int


class TaskDoneCreate(BaseModel):
    user_id: int
    task_id: int


class TaskRead(BaseModel):
    id: int = Field(serialization_alias='key')
    difficult: int
    name: Optional[str] = Field(serialization_alias='title')
    description: Optional[str]
    time: Optional[str]
    solvers: int
    done: bool

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    difficult: Optional[int] = Field(None)
    time: Optional[str] = Field(None)
    solvers: Optional[int] = Field(None)
