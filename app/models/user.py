from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy_utils import ChoiceType

from app.core.db import Base
from app.core.constants import Role

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


class User(SQLAlchemyBaseUserTable[int], Base):
    ROLES = [(role.name, role.value) for role in Role]
    role: Mapped[str] = Column(
        ChoiceType(ROLES), default='user', nullable=False
    )
    username: Mapped[str] = Column(String(length=100), nullable=False)
    tariff_id: Mapped[int] = Column(
        ForeignKey("tariff.id"),
    )
    tariff: Mapped[Tariff] = relationship(back_populates="users")
    profile: Mapped[Profile] = relationship(back_populates="user")
    groups: Mapped[list[Group]] = relationship(
        secondary=group_user_association, back_populates="users"
    )
    notifications: Mapped[Notification] = relationship(
        secondary=notification_user_association, back_populates="users"
    )
    examinations: Mapped[list[Examination]] = relationship(
        secondary=examination_user_association, back_populates="users"
    )
    courses: Mapped[list[Course]] = relationship(
        secondary=course_user_association, back_populates="users"
    )

    def __repr__(self):
        return self.username
