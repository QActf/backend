# from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.core.db import Base
# from app.core.config import settings
from app.models.associations import group_user_association
from app.models.base import AbstractBaseMixin


class Group(AbstractBaseMixin, Base):
    # name = Column(
    #     String(length=settings.max_length_string),
    #     unique=True,
    #     nullable=False
    # )
    # description = Column(Text)
    users = relationship('User', secondary=group_user_association,
                         back_populates='groups')
