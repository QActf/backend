from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, String, Text, ForeignKey

from app.core.db import Base
from .abstract import SomeTask, SomeTaskUserAssociation


class TaskTestUserAssocation(SomeTaskUserAssociation):
    """Модель тестов АПИ - пользователей."""

    answer: str = Column(String, nullable=False)
    task: Mapped['TaskTest'] = Column(ForeignKey('task_api.id'))


class Test(Base):
    """Модель вопроса теста."""

    users: Mapped[list[TaskTestUserAssocation]] = relationship(
        back_populates='tests',
    )


class TaskTest(SomeTask):
    """Модель всего теста."""

    __tablename__ = 'task_test'

    tests = Mapped[list[Test]] = relationship(
        back_populates='task_test'
    )
