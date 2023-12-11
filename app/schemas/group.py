from typing import Optional, List

from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str
    description: Optional[str]


class GroupRead(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True
