from typing import Optional

from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str
    description: Optional[str]


class GroupRead(BaseModel):
    name: Optional[str]
    description: Optional[str]
