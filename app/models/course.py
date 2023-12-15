from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (Column, String, Text, Table, ForeignKey, Integer,
                        UniqueConstraint)
from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base
from app.core.config import settings

if TYPE_CHECKING:
    from app.models import User


course_user_association = Table(
    'course_user_association', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('course_id', ForeignKey('course.id')),
    Column('user_id', ForeignKey('user.id')),
    UniqueConstraint('course_id', 'user_id',
                     name='constraint_course_user')
)


class Course(Base):
    name: str = Column(String(length=settings.max_length_string), unique=True,
                       nullable=False)
    description: str = Column(Text)
    users: Mapped[list[User]] = relationship(
        secondary=course_user_association,
        back_populates='courses'
    )
