from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey, Integer, String, Table, Text, func,
)
from sqlalchemy.orm import Mapped, relationship

from app.core.config import settings
from app.core.db import Base

if TYPE_CHECKING:
    from app.models import User

notification_user_association = Table(
    'notification_user_association',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('notification_id', ForeignKey('notification.id')),
    Column('user_id', ForeignKey('user.id')),
    Column('viewed', Boolean, default=False),
    Column('date', DateTime, default=func.now()),
)


class Notification(Base):
    name: str = Column(
        String(length=settings.max_length_string),
        unique=True,
        nullable=False,
    )
    message: str = Column(Text, nullable=False)
    users: Mapped[list[User]] = relationship(
        secondary=notification_user_association,
        back_populates='notifications',
    )

    def __repr__(self):
        return self.name
