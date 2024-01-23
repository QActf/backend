from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import Mapped, relationship

from app.core.config import settings
from app.core.db import Base

from .course import course_tariff_association

if TYPE_CHECKING:
    from .course import Course
    from .user import User


class Tariff(Base):
    name: Mapped[str] = Column(
        String(length=settings.max_length_string), unique=True, nullable=False
    )
    description: Mapped[str] = Column(Text)
    users: Mapped[list[User]] = relationship(back_populates="tariff")
    courses: Mapped[list[Course]] = relationship(
        secondary=course_tariff_association, back_populates="tariffs"
    )

    def __repr__(self):
        return self.name
