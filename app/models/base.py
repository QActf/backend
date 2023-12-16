from sqlalchemy import Column, String, Text

from app.core.config import settings


class AbstractBaseMixin(object):
    name = Column(
        String(length=settings.max_length_string),
        unique=True,
        nullable=False
    )
    description = Column(Text)
