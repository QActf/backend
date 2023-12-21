from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, relationship

from app.core.config import settings
from app.core.db import Base

if TYPE_CHECKING:
    from app.models import User


notification_user_association = Table(
    'notification_user_association', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('notification_id', ForeignKey('notification.id')),
    Column('user_id', ForeignKey('user.id')),
    UniqueConstraint('notification_id', 'user_id',
                     name='constraint_notification_user')
)


class Notification(Base):
    name: str = Column(String(length=settings.max_length_string), unique=True,
                       nullable=False)
    description: str = Column(Text)
    users: Mapped[list[User]] = relationship(
        secondary=notification_user_association,
        back_populates='notifications'
    )
