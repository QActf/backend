from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config import settings


class NameMixin:
    name: Mapped[str] = mapped_column(
        String(length=settings.max_length_string),
        unique=True,
        nullable=False
    )


class DescriptionMixin:
    description: Mapped[str] = mapped_column(Text)


class NameDescriptionMixin(NameMixin, DescriptionMixin):
    pass
