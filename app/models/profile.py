from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, String, SmallInteger, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base
from app.core.config import settings
from .achievement import achievement_profile_association

if TYPE_CHECKING:
    from .user import User
    from .achievement import Achievement


class Profile(Base):
    first_name: Mapped[str] = Column(String(length=settings.max_length_string))
    last_name: Mapped[str] = Column(String(length=settings.max_length_string))
    age: Mapped[int] = Column(SmallInteger)
    user_id: Mapped[int] = Column(
        ForeignKey('user.id'), unique=True
    )
    user: Mapped[User] = relationship(back_populates='profile')
    achievements: Mapped[Achievement] = relationship(
        secondary=achievement_profile_association,
        back_populates='profiles'
    )
    image: Mapped[str] = Column(
        String(),
        nullable=True,
        default=f'{settings.media_url}cat1.png'
    )
