from typing import TYPE_CHECKING

from sqlalchemy import Column, String, SmallInteger, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base
from app.core.config import settings

if TYPE_CHECKING:
    from .user import User


class Profile(Base):
    first_name: Mapped[str] = Column(String(length=settings.max_length_string))
    last_name: Mapped[str] = Column(String(length=settings.max_length_string))
    age: Mapped[int] = Column(SmallInteger)
    user_id: Mapped[int] = Column(
        ForeignKey('user.id'), unique=True
    )
    user: Mapped['User'] = relationship(back_populates='profile')
