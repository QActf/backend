import enum

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Enum, Column, String
from sqlalchemy.orm import Mapped

from app.core.db import Base


class UserRoleEnum(enum.Enum):
    user = 'user'
    manager = 'manager'
    admin = 'admin'


class User(SQLAlchemyBaseUserTable[int], Base):
    role: Mapped[str] = Column(
        Enum(UserRoleEnum), default=UserRoleEnum.user, nullable=False
    )
    username: Mapped[str] = Column(String(length=100), nullable=False)
