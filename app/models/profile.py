from sqlalchemy import Column, String, SmallInteger
from sqlalchemy.orm import Mapped

from app.core.db import Base
from app.core.config import settings


class Profile(Base):
    first_name: Mapped[str] = Column(String(length=settings.max_length_string))
    last_name: Mapped[str] = Column(String(length=settings.max_length_string))
    age: Mapped[int] = Column(SmallInteger)
