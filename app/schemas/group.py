from typing import Optional

from pydantic import BaseModel, Field


class GroupCreate(BaseModel):
    name: str
    description: Optional[str]


class GroupRead(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True


class GroupUpdate(BaseModel):
    name: Optional[str] = Field(None,)
    description: Optional[str] = Field(None,)
