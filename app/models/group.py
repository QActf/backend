from __future__ import annotations

from typing import List, TYPE_CHECKING

from sqlalchemy import (Column, String, Text, Table, ForeignKey, Integer,
                        UniqueConstraint)
from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base
from app.core.config import settings

if TYPE_CHECKING:
    from app.models import User


group_user_association = Table(
    'group_user_association', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('group_id', ForeignKey('group.id')),
    Column('user_id', ForeignKey('user.id')),
    UniqueConstraint('group_id', 'user_id', name='constraint_group_user')
)


class Group(Base):
    name: str = Column(String(length=settings.max_length_string), unique=True,
                       nullable=False)
    description: str = Column(Text)
    users: Mapped[List[User]] = relationship(secondary=group_user_association,
                                             back_populates='groups')
