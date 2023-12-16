from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models.base import AbstractBaseMixin
from app.models.associations import course_task_association


class Task(AbstractBaseMixin, Base):
    courses = relationship(
        'Course',
        secondary=course_task_association,
        back_populates='tasks'
    )
