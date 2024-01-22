from typing import Optional

from pydantic import BaseModel


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
    name: str
    description: str
