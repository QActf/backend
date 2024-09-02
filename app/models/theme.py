from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

from .mixins import NameMixin

if TYPE_CHECKING:
    from .themescategory import ThemesCategory


class Theme(Base, NameMixin):
    themescategory_id: Mapped[int] = mapped_column(
        ForeignKey('themescategory.id')
    )
    themescategory: Mapped[ThemesCategory] = relationship(
        back_populates='themes'
    )
