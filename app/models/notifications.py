from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models.associations import user_notification_association


class Notification(Base):
    users = relationship(
        'User', secondary=user_notification_association,
        back_populates='notifications'
    )
