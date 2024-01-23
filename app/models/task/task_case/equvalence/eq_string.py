from sqlalchemy import Column, String

from app.core.db import Base


class StringRangeEquvalence(Base):
    """Эквивалетных класс строк - диапазон значений."""

    __tablename__ = 'task_case_equvalence_string_range'

    regular: str = Column(String)


class StringConcreteEquvalence(Base):
    """Эквивалетных класс строк - конкретное значение."""

    __tablename__ = 'task_case_equvalence_string_concrete'

    value: str = Column(String)
