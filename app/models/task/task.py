"""
Любая задача = тестирование чего-то
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Column
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import (Float, ForeignKey, Integer, String, Table, Text,
                        UniqueConstraint)
from sqlalchemy.orm import Mapped, relationship

from app.core.config import settings
from app.core.db import Base

from .abstract import SomeTask
from .task_api import TaskAPI  # noqa
from .task_case import TaskCase  # noqa
from .task_db import TaskDB  # noqa
from .task_test import TaskTest  # noqa

if TYPE_CHECKING:
    from ..user import Course


task_course_association = Table(
    'task_course_association', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('task_id', ForeignKey('task.id')),
    Column('course_id', ForeignKey('course.id')),
    UniqueConstraint('task_id', 'course_id',
                     name='constraint_task_course')
)


class TaskTypes(Enum):
    """Тип задач."""

    task_case = 'TaskCase'
    task_api = 'TaskAPI'
    task_db = 'TaskDB'
    task_test = 'TaskTest'


TASK_CLASSES = {
    TaskTypes.task_case: TaskCase,
    TaskTypes.task_api: TaskAPI,
    TaskTypes.task_db: TaskDB,
    TaskTypes.task_test: TaskTest,
}


class Task(Base):
    """Модель БД задач."""

    __tablename__ = 'task'

    name: str = Column(
        String(length=settings.max_length_string),
        unique=True,
        nullable=False,
    )
    short_description: str = Column(Text, nullable=False)
    full_description: str = Column(Text, nullable=False)
    avg_time: float = Column(Float)
    type_task: TaskTypes = Column(SqlEnum(TaskTypes), nullable=False)
    courses: Mapped[list[Course]] = relationship(
        secondary=task_course_association,
        back_populates='tasks',
    )

    @staticmethod
    def get_concrete_task(type_task: TaskTypes) -> SomeTask:
        """Возвращает модель конретного типа задач."""
        return TASK_CLASSES[type_task.value]
