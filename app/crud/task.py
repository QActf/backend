from app.crud.base import CRUDBase
from app.models import Task


class CRUDTask(CRUDBase):
    pass


task_crud = CRUDTask(Task)
