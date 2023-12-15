from typing import Optional

from pydantic import BaseModel


class NotificationCreate(BaseModel):
    name: str
    description: Optional[str]


class NotificationRead(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True
