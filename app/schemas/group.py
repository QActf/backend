from typing import Optional

from pydantic import BaseModel, Field


class GroupCreate(BaseModel):
    name: str = Field(..., example="Название группы")
    description: Optional[str] = Field(..., example="Описание группы")


class GroupRead(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True


class GroupUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Название группы")
    description: Optional[str] = Field(None, example="Описание группы")
