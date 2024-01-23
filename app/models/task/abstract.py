from typing import TYPE_CHECKING

from sqlalchemy import Integer
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.user import User


class SomeTaskUserAssociation(AbstractConcreteBase, Base):
    """АК для ассоциаций задач-пользователей."""

    __abstract__ = True
    scores: Mapped['Integer'] = mapped_column(Integer, default=0)
    user: Mapped['User']
    task: Mapped['SomeTask']


class SomeTask(AbstractConcreteBase, Base):
    """АК конкретной задачи."""

    __abstract__ = True
    task_id: Mapped['Integer'] = mapped_column(Integer, nullable=False,)
