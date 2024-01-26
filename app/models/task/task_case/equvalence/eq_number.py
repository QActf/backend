from sqlalchemy import Boolean, Column, Float

from app.core.db import Base


class NumbRangeEquvalence(Base):
    """Эквивалетных класс чисел - диапазон значений."""

    __tablename__ = 'task_case_equvalence_numb_range'

    min_numb: float = Column(Float, default=0.0)
    max_numb: float = Column(Float, nullable=False)
    is_float: bool = Column(Boolean, default=True)


class NumbConcreteEquvalence(Base):
    """Эквивалетных класс чисел - конкретное значение."""

    __tablename__ = 'task_case_equvalence_numb_concrete'

    value: float = Column(Float, nullable=False)
