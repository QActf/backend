from sqlalchemy import Column, String, Text
from sqlalchemy.orm import Mapped

from app.core.db import Base
from app.core.config import settings


class Tariff(Base):
    name: Mapped[str] = Column(String(length=settings.max_length_string),
                               unique=True, nullable=False)
    description: Mapped[str] = Column(Text)
