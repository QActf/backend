from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models.base import AbstractBaseMixin
from app.models.associations import course_tariff_association


class Tariff(AbstractBaseMixin, Base):
    courses = relationship(
        'Course',
        secondary=course_tariff_association,
        back_populates='tariffs'
    )
    users = relationship('User', back_populates='tariff')
