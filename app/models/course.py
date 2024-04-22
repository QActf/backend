from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String, Table, Text, UniqueConstraint
)
from sqlalchemy.orm import Mapped, relationship

from app.core.config import settings
from app.core.db import Base

from .task import task_course_association

if TYPE_CHECKING:
    from .tariff import Tariff
    from .task import Task
    from .user import User


course_user_association = Table(
    "course_user_association",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("course_id", ForeignKey("course.id")),
    Column("user_id", ForeignKey("user.id")),
    UniqueConstraint("course_id", "user_id", name="constraint_course_user"),
)

course_tariff_association = Table(
    "course_tariff_association",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("course_id", ForeignKey("course.id")),
    Column("tariff_id", ForeignKey("tariff.id")),
    UniqueConstraint(
        "course_id", "tariff_id", name="constraint_course_tariff"
    ),
)


class Course(Base):
    name: str = Column(
        String(length=settings.max_length_string), unique=True, nullable=False
    )
    description: str = Column(Text)
    is_closed: bool = Column(Boolean, default=False)
    users: Mapped[list[User]] = relationship(
        secondary=course_user_association, back_populates="courses"
    )
    tariffs: Mapped[list[Tariff]] = relationship(
        secondary=course_tariff_association, back_populates="courses"
    )
    tasks: Mapped[list[Task]] = relationship(
        secondary=task_course_association, back_populates="courses"
    )

    def __repr__(self):
        return self.name
