from __future__ import annotations

from typing import List

from sqlalchemy import Column, String, Text, Table, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base
from app.core.config import settings
from app.models import User


association_table = Table(
    'association_table', Base.metadata,
    Column('group_id', ForeignKey('group.id')),
    Column('user_id', ForeignKey('user.id'))
)


class Group(Base):
    name: str = Column(String(length=settings.max_length_string), unique=True,
                       nullable=False)
    description: str = Column(Text)
    user: Mapped[List[User]] = relationship(secondary=association_table)
