from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Column
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship

from app.core.config import settings
from app.core.db import Base

from .equvalence import EquvalenceField

if TYPE_CHECKING:
    from .case import TaskCase


class TypeField(Enum):
    """Енам типов полей."""

    NUMBER = 'number'
    STRING = 'string'
    CHOISE = 'choise'
    CHECK_BOX = 'check_box'


class Field(Base):
    """Модель образа поля."""

    __tablename__ = 'task_case_field'

    case: Mapped['TaskCase'] = relationship(
        back_populates='fields',
    )
    type_field: TypeField = Column(SqlEnum(TypeField), nullable=False)
    name: str = Column(String(settings.max_length_string), nullable=False)
    equvalences: Mapped[list['EquvalenceField']] = relationship(
        back_populates='field',
    )


class ChioseValue(Base):
    """Значения для поля выбора."""

    __tablename__ = 'task_case_choise_value'

    field: Mapped['Field'] = relationship(
        back_populates='values',
    )
    value: str = Column(String(settings.max_length_string), nullable=False)
