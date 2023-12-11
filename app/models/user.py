import enum

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Enum, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from app.core.db import Base
from app.models.associations import (
    group_user_association, user_notification_association
)


class UserRoleEnum(enum.Enum):
    user = 'user'
    manager = 'manager'
    admin = 'admin'


class User(SQLAlchemyBaseUserTable[int], Base):
    role = Column(
        Enum(UserRoleEnum), default=UserRoleEnum.user, nullable=False
    )
    username = Column(String(length=100), nullable=False)
    groups = relationship(
        'Group', secondary=group_user_association,
        back_populates='users'
    )
    course_usercourse = relationship('UserCourse', back_populates='user')
    examination_userexamination = relationship(
        'UserExamination', back_populates='user'
    )
    notifications = relationship(
        'Notification', secondary=user_notification_association,
        back_populates='users'
    )
    profile = relationship("Profile", uselist=False, back_populates='user')

    tariff_id = Column(Integer, ForeignKey('tariff.id'))
    tariff = relationship('Tariff', back_populates='users')
