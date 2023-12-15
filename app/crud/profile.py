from app.crud.base import CRUDBase
from app.models import Profile


class CRUDNotification(CRUDBase):
    pass


profile_crud = CRUDNotification(Profile)
