from sqlalchemy import Column, String, Text

from app.core.config import settings
from app.core.db import Base


class Question(Base):
    problem: str = Column(
        String(length=settings.max_length_string), unique=True, nullable=False
    )
    solution: str = Column(Text)

    def __repr__(self):
        return self.name
