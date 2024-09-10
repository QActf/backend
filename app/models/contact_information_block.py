from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import EmailType, PhoneNumberType, ScalarListType

from app.core.db import Base


class ContactInformationBlock(Base):
    phones: Mapped[list[str]] = mapped_column(
        ARRAY(PhoneNumberType())
        .with_variant(ScalarListType(), 'postgresql')
    )
    email: Mapped[str] = mapped_column(EmailType)
