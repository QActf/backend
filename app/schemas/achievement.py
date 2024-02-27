from typing import Optional

from pydantic import BaseModel, Field


class AchievementCreate(BaseModel):
    name: str
    description: Optional[str]


class AchievementRead(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True


class AchievementUpdate(BaseModel):
    name: Optional[str] = Field(None,)
    description: Optional[str] = Field(None,)
