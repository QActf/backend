from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import (Column, String, Float, Boolean, Integer)

from app.core.db import Base
from app.models.user import User
from app.core.config import settings
from .abstract import SomeTask, SomeTaskUserAssociation


class TaskFieldUserAssocation(SomeTaskUserAssociation):
    task


class AbstractField(Base):
    __abstract__ = True
    name: str = Column(String(length=settings.max_length_string), nullable=False)
    users: Mapped[list[TaskFieldUserAssocation]]


class NumbField(AbstractField):
    users = 
    max_numb: int = Column(Float)
    min_numb: int = Column(Float)
    is_float: bool = Column(Boolean)


class Choises(Base):
    name: str = Column(String(length=settings.max_length_string), nullable=False)


class ChoiseField(AbstractField):
    users = 
    values: Mapped[list[Choises]] = relationship(
        back_populates='choise_field'
    )


class CheckField(AbstractField):
    users = 


class StringField(AbstractField):
    users = 
    max_lenght: int = Column(Integer)
    min_lenght: int = Column(Integer)
    regular: str = Column(String)





class TaskCase(SomeTask):
    """Тест-кейс."""

    fields: Mapped[list['helpPlZ']] = relationship(
        back_populates='task_case'
    )
