from sqlalchemy import Column, String, SmallInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.core.config import settings
from app.models.associations import achievement_profile_association


class Profile(Base):
    first_name = Column(String(length=settings.max_length_string))
    second_name = Column(String(length=settings.max_length_string))
    age = Column(SmallInteger)
    achievements = relationship(
        'Achievement',
        secondary=achievement_profile_association,
        back_populates='profiles'
    )
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates="profile")
