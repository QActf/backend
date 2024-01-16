from __future__ import annotations

from pathlib import Path
from random import randint
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, SmallInteger, String
from sqlalchemy.orm import Mapped, relationship

from app.core.config import settings
from app.core.db import Base

from .achievement import achievement_profile_association

if TYPE_CHECKING:
    from .achievement import Achievement
    from .user import User


def _random_photo(path: Path):
    """Возвращает рандомный файл из указанной папки."""
    files = [f'cats/{file.name}' for file in path.iterdir()]
    random_index = randint(0, len(files) - 1)
    return str(files[random_index])


class Profile(Base):
    first_name: Mapped[str] = Column(
        String(length=settings.max_length_string)
    )
    last_name: Mapped[str] = Column(
        String(length=settings.max_length_string)
    )
    age: Mapped[int] = Column(
        SmallInteger
    )
    user_id: Mapped[int] = Column(
        ForeignKey('user.id'), unique=True
    )
    user: Mapped[User] = relationship(back_populates='profile')
    achievements: Mapped[Achievement] = relationship(
        secondary=achievement_profile_association, back_populates="profiles"
    )
    image: Mapped[str] = Column(
        String(),
        nullable=True,
        default=_random_photo(settings.base_dir / settings.media_url / 'cats/')
    )

    def __repr__(self):
        return self.first_name
