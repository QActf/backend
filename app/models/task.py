from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (Column, ForeignKey, Integer, String, Table, Text,
                        UniqueConstraint)
from sqlalchemy.orm import Mapped, relationship

from app.core.config import settings
from app.core.db import Base

if TYPE_CHECKING:
    from .user import Course


task_course_association = Table(
    "task_course_association",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("task_id", ForeignKey("task.id")),
    Column("course_id", ForeignKey("course.id")),
    UniqueConstraint("task_id", "course_id", name="constraint_task_course"),
)


class Task(Base):
    name: str = Column(
        String(length=settings.max_length_string), unique=True, nullable=False
    )
    description: str = Column(Text)
    courses: Mapped[list[Course]] = relationship(
        secondary=task_course_association, back_populates="tasks"
    )
