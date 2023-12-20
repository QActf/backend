from enum import Enum

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, String, Text, ForeignKey, Enum as SqlEnum

from .abstract import SomeTask, SomeTaskUserAssociation


class TaskDBUserAssocation(SomeTaskUserAssociation):
    """Модель тестов БД - пользователей"""

    response_user: str = Column(String, nullable=False)
    task: Mapped['TaskDB'] = Column(ForeignKey('task_db.id'))


class TestDataBase(Enum):
    test = 'test'


class TaskDB(SomeTask):
    """Тестирование API."""

    __tablename__ = 'task_db'

    data_base: str = Column(String, nullable=False)
    request: str = Column(Text, nullable=False)
    response: str = Column(Text, nullable=False)
    answer: str = Column(Text, nullable=False)
    users: Mapped[list[TaskDBUserAssocation]] = relationship(
        back_populates='task_db',
    )
