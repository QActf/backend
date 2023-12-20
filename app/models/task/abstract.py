from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped

from app.models.user import User
from app.core.db import Base


class SomeTaskUserAssociation(Base):
    """АК для ассоциаций задач-пользователей."""

    __abstract__ = True
    scores: int = Column(Integer, default=0)
    user: Mapped[User] = Column(ForeignKey('user.id'))
    task: Mapped['SomeTask']


class SomeTask(Base):
    """АК конкретной задачи."""

    __abstract__ = True
    task_id: int = Column(Integer, nullable=False,)
