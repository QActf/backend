from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.achievement import AchievementRead


class ProfileRead(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    age: Optional[int]
    user_id: int
    image: Optional[str]
    # achievements: Optional[list[AchievementRead]]

    class Config:
        from_attributes = True


class ProfileCreate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    age: Optional[int]
    user_id: int


class ProfileUpdate(BaseModel):
    first_name: Optional[str] = Field(None,)
    last_name: Optional[str] = Field(None,)
    age: Optional[int] = Field(None,)
