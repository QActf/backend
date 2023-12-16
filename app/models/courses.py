from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models.base import AbstractBaseMixin
from app.models.associations import (
    course_task_association, course_tariff_association
)


class Course(AbstractBaseMixin, Base):
    tasks = relationship(
        'Task',
        secondary=course_task_association,
        back_populates='courses'
    )
    user_usercourse = relationship('UserCourse', back_populates='course')
    tariffs = relationship(
        'Tariff',
        secondary=course_tariff_association,
        back_populates='courses'
    )
