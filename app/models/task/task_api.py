from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, String, Text, ForeignKey

from .abstract import SomeTask, SomeTaskUserAssociation

if TYPE_CHECKING:
    from app.models.user import User


class TaskAPIUserAssociation(SomeTaskUserAssociation):
    """Модель тестов АПИ - пользователей."""

    __tablename__ = 'task_api_user_assoc'

    url_user: str = Column(String, nullable=False)
    body_user: str = Column(Text, nullable=False)
    response_user: str = Column(String, nullable=False)
    task: Mapped['TaskAPI'] = Column(ForeignKey('task_api.id'))
    user: Mapped['User'] = Column(ForeignKey('user.id'))


class TaskAPI(SomeTask):
    """Тестирование API."""

    __tablename__ = 'task_api'

    url: str = Column(String, nullable=False)
    body: str = Column(Text, nullable=False)
    response: str = Column(Text, nullable=False)
    users: Mapped[list['TaskAPIUserAssociation']] = relationship(
        back_populates='task_api',
    )
