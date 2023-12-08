from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models.base import AbstractBaseMixin


class Examination(AbstractBaseMixin, Base):
    user_userexamination = relationship(
        'UserExamination', back_populates='examination'
    )
