from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, ForeignKey

from ..abstract import SomeTask, SomeTaskUserAssociation
from .field import Field
from .instance import Instance

if TYPE_CHECKING:
    from app.models.user import User


class CaseUserAssociation(SomeTaskUserAssociation):
    """Ассациация пользователей и тест-кейсов."""

    __tablename__ = 'task_case_user_assoc'

    task: Mapped['TaskCase'] = Column(ForeignKey('task_case.id'))
    instances: Mapped[list['Instance']] = relationship(
        back_populates='user_case',
    )
    user: Mapped['User'] = Column(ForeignKey('user.id'))


class TaskCase(SomeTask):
    """Модель тест-кейсов."""

    __tablename__ = 'task_case'

    fields: Mapped[list['Field']] = relationship(
        back_populates='case'
    )
    users: Mapped[list['CaseUserAssociation']] = relationship(
        back_populates='task_case',
    )
