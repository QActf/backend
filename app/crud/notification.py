from app.crud.base import CRUDBase
from app.models import Notification


class CRUDNotification(CRUDBase):
    pass


notification_crud = CRUDNotification(Notification)
