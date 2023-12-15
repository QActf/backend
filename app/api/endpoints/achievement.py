from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import achievement_crud
from app.schemas.achievement import AchievementCreate, AchievementRead


router = APIRouter()


@router.post('/')
async def create_achievement(
    achievement: AchievementCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await achievement_crud.create(achievement, session)


@router.get('/', response_model=list[AchievementRead])
async def get_all_achievements(
    session: AsyncSession = Depends(get_async_session)
):
    return await achievement_crud.get_multi(session)
