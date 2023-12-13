from app.crud.base import CRUDBase
from app.models import Course


class CRUDCourse(CRUDBase):
    pass


course_crud = CRUDCourse(Course)
