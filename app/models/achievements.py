from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models.base import AbstractBaseMixin
from app.models.associations import achievement_profile_association


class Achievement(AbstractBaseMixin, Base):
    profiles = relationship(
        'Profile',
        secondary=achievement_profile_association,
        back_populates='profiles'
    )
