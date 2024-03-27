from typing import Optional

from pydantic import BaseModel, Field


class AchievementCreate(BaseModel):
    name: str = Field(..., example="Название достижения")
    description: Optional[str] = Field(..., example="Описание достижения")


class AchievementRead(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True


class AchievementUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Название достижения")
    description: Optional[str] = Field(None, example="Описание достижения")
