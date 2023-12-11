import enum
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Enum, Column, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from .tariff import Tariff


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
