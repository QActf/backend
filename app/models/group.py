from sqlalchemy import Column, String, Text

from app.core.db import Base
from app.core.config import settings


class Group(Base):
    name = Column(String(length=settings.max_length_string), unique=True,
                  nullable=False)
    description = Column(Text)
