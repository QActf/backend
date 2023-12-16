from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base
from app.core.config import settings
from .course import course_tariff_association

if TYPE_CHECKING:
    from .user import User
    from .course import Course


class Tariff(Base):
    name: Mapped[str] = Column(String(length=settings.max_length_string),
                               unique=True, nullable=False)
    description: Mapped[str] = Column(Text)
    users: Mapped[list[User]] = relationship(back_populates='tariff')
    courses: Mapped[list[Course]] = relationship(
        secondary=course_tariff_association,
        back_populates='tariffs'
    )
