from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models import Achievement, Profile
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class CRUDAchievement(CRUDBase):
    async def get(self, obj_id: int, session: AsyncSession):
        stmt = (
            select(Achievement)
            .where(Achievement.id == obj_id)
            .options(
                selectinload(Achievement.profiles)
            )
        )
        achievement = await session.execute(stmt)
        achievement = achievement.scalars().first()
        return achievement

    async def get_users_obj(self, user_id: int, session: AsyncSession):
        stmt = (
            select(Achievement)
            .options(
                selectinload(Achievement.profiles)
            ).where(Achievement.profiles.any(Profile.user_id == user_id))
        )
        db_obj = await session.execute(stmt)
        return db_obj.scalars().all()


achievement_crud = CRUDAchievement(Achievement)
