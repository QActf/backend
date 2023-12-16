from typing import Optional

from pydantic import BaseModel


class ProfileRead(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    age: Optional[int]
    user_id: int

    class Config:
        from_attributes = True


class ProfileCreate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    age: Optional[int]
    user_id: int
