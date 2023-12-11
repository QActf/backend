from app.crud.base import CRUDBase
from app.models import Examination


class CRUDExamination(CRUDBase):
    pass


examination_crud = CRUDExamination(Examination)
