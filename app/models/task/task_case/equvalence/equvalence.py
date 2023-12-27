from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped
from sqlalchemy import (
    Column, Enum as SqlEnum,
    ForeignKey, Integer
)

from app.core.db import Base
from .eq_number import NumbConcreteEquvalence, NumbRangeEquvalence
from .eq_string import StringConcreteEquvalence, StringRangeEquvalence

if TYPE_CHECKING:
    from ..field import Field


class EquvalenceType(Enum):
    """Типы задания классов эквивалетности."""

    RANGE = 'range'
    CONCRETE = 'concrete'


class EqFieldType(Enum):
    """Типы полей, которым необходимо задавать классы эквивалентности."""

    NUMBER = 'number'
    STRING = 'string'


EQUVALENCE_CLASSES = {
    'number_range': NumbRangeEquvalence,
    'number_concrete': NumbConcreteEquvalence,
    'string_range': StringRangeEquvalence,
    'string_concrete': StringConcreteEquvalence,
}

class EquvalenceField(Base):
    """Модель связи конкретного эквивалетного случая поля."""

    __tablename__ = 'task_case_equvalence_field'

    field: Mapped['Field'] = Column(ForeignKey('task_case_field.id'))
    equvalence: int = Column(Integer, nullable=False)
    type_equvalence: EquvalenceType = Column(
        SqlEnum(EquvalenceType),
        default=EquvalenceType.CONCRETE
    )

    @staticmethod
    def get_equvalence(type_eq: EquvalenceType, type_var: EqFieldType):
        return EQUVALENCE_CLASSES[f"{type_var.value}_{type_eq.value}"]
