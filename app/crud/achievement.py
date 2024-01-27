from app.crud.base import CRUDBase
from app.models import Achievement, Profile


class CRUDAchievement(CRUDBase):
    async def get_users_achievement(
            self,
            obj_id: int,
            profile: Profile,
    ):
        achievements: list[Achievement] = profile.achievements
        try:
            achievement = list(
                filter(
                    lambda achievement: achievement.id == obj_id, achievements
                )
            )[0]
        except IndexError:
            return {
                "detail": f"Объект achievement с id {obj_id} не найден."
            }
        return achievement


achievement_crud = CRUDAchievement(Achievement)
