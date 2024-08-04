from datetime import datetime

from pydantic import BaseModel


class NotificationCreate(BaseModel):
    name: str
    message: str


class NotificationRead(BaseModel):
    id: int
    name: str
    message: str


class AddNotificationForUser(BaseModel):
    user_id: int
    notification_id: int


class ReadNotificationForUser(BaseModel):
    id: int
    name: str
    message: str = None
    date: datetime

    class Config:
        from_attributes = True
