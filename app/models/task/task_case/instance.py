from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, String, ForeignKey, Boolean

from app.core.db import Base
from .equvalence import EquvalenceField

if TYPE_CHECKING:
    from .field import Field
    from .case import CaseUserAssociation


class InstanceFieldAssociation(Base):
    """Ассоциация конкретных примеров и полей кейса."""

    __tablename__ = 'task_case_instance_field'

    instance: Mapped['Instance'] = ForeignKey('task_case_instance.id')
    field: Mapped['Field'] = ForeignKey('task_case_field.id')
    value: str = Column(String, nullable=False)
    equvalence: Mapped['EquvalenceField'] = relationship(
        back_populates='instances',
    )


class Instance(Base):
    """Модель кейса пользователя."""

    __tablename__ = 'task_case_instance'

    user_case: Mapped['CaseUserAssociation'] = relationship(
        back_populates='instances',
    )
    fields: Mapped[list['InstanceFieldAssociation']] = relationship(
        back_populates='instances',
    )
    correctly: bool = Column(Boolean, default=False)
