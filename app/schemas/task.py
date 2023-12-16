from typing import Optional

from pydantic import BaseModel


class TaskCreate(BaseModel):
    name: str
    description: Optional[str]


class TaskRead(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True
