from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, String, Text, ForeignKey

from .abstract import SomeTask, SomeTaskUserAssociation


class TaskAPIUserAssocation(SomeTaskUserAssociation):
    """Модель тестов АПИ - пользователей."""

    response_user: str = Column(String, nullable=False)
    task: Mapped['TaskAPI'] = Column(ForeignKey('task_api.id'))


class TaskAPI(SomeTask):
    """Тестирование API."""

    __tablename__ = 'task_api'

    url: str = Column(String, nullable=False)
    body: str = Column(Text, nullable=False)
    response: str = Column(Text, nullable=False)
    answer: str = Column(Text, nullable=False)
    users: Mapped[list[TaskAPIUserAssocation]] = relationship(
        back_populates='task_api',
    )
