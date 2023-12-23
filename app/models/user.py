from __future__ import annotations

import hashlib

import bcrypt
import enum
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base

from .course import course_user_association
from .examination import examination_user_association
from .group import group_user_association
from .notification import notification_user_association

if TYPE_CHECKING:
    from .course import Course
    from .examination import Examination
    from .group import Group
    from .notification import Notification
    from .profile import Profile
    from .tariff import Tariff


class UserRoleEnum(enum.Enum):
    user = "user"
    manager = "manager"
    admin = "admin"


class User(SQLAlchemyBaseUserTable[int], Base):
    role: Mapped[str] = Column(
        Enum(UserRoleEnum), default=UserRoleEnum.user, nullable=False
    )
    username: Mapped[str] = Column(String(length=100), nullable=False)
    tariff_id: Mapped[int] = Column(
        ForeignKey("tariff.id"),
    )
    tariff: Mapped[Tariff] = relationship(back_populates="users")
    profile: Mapped[Profile] = relationship(back_populates="user")
    groups: Mapped[Group] = relationship(
        secondary=group_user_association, back_populates="users"
    )
    notifications: Mapped[Notification] = relationship(
        secondary=notification_user_association, back_populates="users"
    )
    examinations: Mapped[Examination] = relationship(
        secondary=examination_user_association, back_populates="users"
    )
    courses: Mapped[Course] = relationship(
        secondary=course_user_association, back_populates="users"
    )

    def __repr__(self):
        return self.username
