from app.crud.base import CRUDBase
from app.models import Question


class CRUDQuestion(CRUDBase):
    pass


question_crud = CRUDQuestion(Question)
