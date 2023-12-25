from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (Column, ForeignKey, Integer, String, Table, Text,
                        UniqueConstraint)
from sqlalchemy.orm import Mapped, relationship

from app.core.config import settings
from app.core.db import Base

if TYPE_CHECKING:
    from app.models import Profile


achievement_profile_association = Table(
    "achievement_profile_association",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("achievement_id", ForeignKey("achievement.id")),
    Column("profile_id", ForeignKey("profile.id")),
    UniqueConstraint(
        "achievement_id", "profile_id",
        name="constraint_achievement_profile"
    ),
)


class Achievement(Base):
    name: str = Column(
        String(length=settings.max_length_string), unique=True, nullable=False
    )
    description: str = Column(Text)
    profiles: Mapped[list[Profile]] = relationship(
        secondary=achievement_profile_association,
        back_populates="achievements"
    )

    def __repr__(self):
        return self.name
