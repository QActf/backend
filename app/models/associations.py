from sqlalchemy import (
    Column, Integer, ForeignKey, Table, SmallInteger
)
from sqlalchemy.orm import relationship

from app.core.db import Base


group_user_association = Table(
    'group_user_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('group_id', Integer, ForeignKey('group.id')),
)

achievement_profile_association = Table(
    'achievement_profile_association', Base.metadata,
    Column('profile_id', Integer, ForeignKey('profile.id')),
    Column('achievement_id', Integer, ForeignKey('achievement.id'))
)
course_task_association = Table(
    'course_task_association', Base.metadata,
    Column('course_id', Integer, ForeignKey('course.id')),
    Column('task_id', Integer, ForeignKey('task.id'))
)
course_tariff_association = Table(
    'course_tariff_association', Base.metadata,
    Column('course_id', Integer, ForeignKey('course.id')),
    Column('tariff_id', Integer, ForeignKey('tariff.id'))
)
user_notification_association = Table(
    'user_notification_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('notification_id', Integer, ForeignKey('notification.id'))
)


class UserCourse(Base):
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'), primary_key=True)
    progress = Column(SmallInteger)
    user = relationship('User', back_populates='course_usercourse')
    course = relationship('Course', back_populates='user_usercourse')


class UserExamination(Base):
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    examination_id = Column(
        Integer, ForeignKey('examination.id'), primary_key=True
    )
    progress = Column(SmallInteger)
    user = relationship('User', back_populates='examination_userexamination')
    examination = relationship(
        'Examination', back_populates='user_userexamination'
    )
