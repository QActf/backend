from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base

from .mixins import NameMixin

if TYPE_CHECKING:
    from .theme import Theme


class ThemesCategory(Base, NameMixin):
    themes: Mapped[list[Theme]] = relationship(back_populates='themescategory')
