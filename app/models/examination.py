from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (Column, String, Text, Table, ForeignKey, Integer,
                        UniqueConstraint)
from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base
from app.core.config import settings

if TYPE_CHECKING:
    from app.models import User


examination_user_association = Table(
    'examination_user_association', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('examination_id', ForeignKey('examination.id')),
    Column('user_id', ForeignKey('user.id')),
    UniqueConstraint('examination_id', 'user_id',
                     name='constraint_examination_user')
)


class Examination(Base):
    name: str = Column(String(length=settings.max_length_string), unique=True,
                       nullable=False)
    description: str = Column(Text)
    users: Mapped[list[User]] = relationship(
        secondary=examination_user_association,
        back_populates='examinations'
    )
