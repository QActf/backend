from app.crud.base import CRUDBase
from app.models import User


class CRUDUser(CRUDBase):
    pass


user_crud = CRUDUser(User)
