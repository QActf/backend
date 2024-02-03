from app.crud.base import CRUDBase
from app.models import Examination, User


class CRUDExamination(CRUDBase):
    async def get_users_examination(
            self,
            obj_id: int,
            user: User,
    ):

        examinations: list[Examination] = user.examinations
        try:
            achievement = list(
                filter(
                    lambda examination: examination.id == obj_id, examinations
                )
            )[0]
        except IndexError or TypeError:
            return {
                "detail": f"Объект examination с id {obj_id} не найден."
            }
        return achievement


examination_crud = CRUDExamination(Examination)
