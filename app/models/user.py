import enum
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Enum, Column, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base
from .group import group_user_association

if TYPE_CHECKING:
    from .tariff import Tariff
    from .profile import Profile
    from .group import Group


class UserRoleEnum(enum.Enum):
    user = 'user'
    manager = 'manager'
    admin = 'admin'


class User(SQLAlchemyBaseUserTable[int], Base):
    role: Mapped[str] = Column(
        Enum(UserRoleEnum), default=UserRoleEnum.user, nullable=False
    )
    username: Mapped[str] = Column(String(length=100), nullable=False)
    tariff_id: Mapped[int] = Column(
        ForeignKey('tariff.id'),
    )
    tariff: Mapped['Tariff'] = relationship(back_populates='users')
    profile: Mapped['Profile'] = relationship(back_populates='user')
    groups: Mapped['Group'] = relationship(secondary=group_user_association,
                                           back_populates='users')
