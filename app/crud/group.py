from app.crud.base import CRUDBase
from app.models.group import Group


class CRUDGroup(CRUDBase):
    pass


group_crud = CRUDGroup(Group)
