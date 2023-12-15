from app.crud.base import CRUDBase
from app.models import Achievement


class CRUDAchievement(CRUDBase):
    pass


achievement_crud = CRUDAchievement(Achievement)
