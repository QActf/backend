from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import EmailType

from app.core.db import Base


class Question(Base):
    from_user_email: Mapped[str] = mapped_column(EmailType)
    message: Mapped[str] = mapped_column(Text)
