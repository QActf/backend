"""
Тестирование БД будет происходить по типу: запрос, ожидание/ответ.
Интерфейса для создани БД не будет.
Надо будет заранее создать и указать в TestDataBase базу данных.
"""

from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, String, Text, ForeignKey, Enum as SqlEnum

from .abstract import SomeTask, SomeTaskUserAssociation

if TYPE_CHECKING:
    from app.models.user import User


class TaskDBUserAssociation(SomeTaskUserAssociation):
    """Модель тестов БД - пользователей"""

    __tablename__ = 'task_db_user_assoc'

    response_user: str = Column(String, nullable=False)
    task: Mapped['TaskDB'] = Column(ForeignKey('task_db.id'))
    user: Mapped['User'] = Column(ForeignKey('user.id'))


class TestDataBase(Enum):
    """Перечисление заготовленных баз данных."""

    test = 'test'


class TaskDB(SomeTask):
    """
    Тестирование баз данных.
      data-base определенная база данных (ее название);
      request - запрос к бд. Идеальный ответ к задаче;
      reponse - ответ с бд. Ответ к задаче (что должен получить пользователь).
    """

    __tablename__ = 'task_db'

    data_base: str = Column(SqlEnum(TestDataBase), nullable=False)
    request: str = Column(Text, nullable=False)
    response: str = Column(Text, nullable=False)
    users: Mapped[list['TaskDBUserAssocation']] = relationship(
        back_populates='task_db',
    )
