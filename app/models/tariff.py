from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base
from app.core.config import settings

if TYPE_CHECKING:
    from .user import User


class Tariff(Base):
    name: Mapped[str] = Column(String(length=settings.max_length_string),
                               unique=True, nullable=False)
    description: Mapped[str] = Column(Text)
    users: Mapped[list['User']] = relationship(back_populates='users')
