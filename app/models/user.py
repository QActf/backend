import enum

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
import sqlalchemy as sa

from app.core.db import Base


class UserRoleEnum(enum.Enum):
    user = 'user'
    manager = 'manager'
    admin = 'admin'


class User(SQLAlchemyBaseUserTable[int], Base):
    role = sa.Column(sa.Enum(UserRoleEnum), default=UserRoleEnum.user,
                     nullable=False)
    username = sa.Column(sa.String(length=100), nullable=False)
