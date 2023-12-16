from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate, check_obj_exists
from app.schemas.achievement import AchievementRead, AchievementCreate
from app.core.db import get_async_session
from app.crud import achievement_crud

router = APIRouter()


@router.get('/', response_model=list[AchievementRead])
async def get_all_achievements(
        session: AsyncSession = Depends(get_async_session)
) -> list[AchievementRead]:
    """Возвращает все achievement."""
    return await achievement_crud.get_multi(session)


@router.post('/', response_model=AchievementRead)
async def create_achievement(
        achievement: AchievementCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Создать Achievement"""
    await check_name_duplicate(achievement.name, achievement_crud, session)
    return await achievement_crud.create(
        obj_in=achievement, session=session
    )


@router.delete('/{obj_id}')
async def delete_achievement(
        obj_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Удалить объект"""
    await check_obj_exists(obj_id, achievement_crud, session)
    achievement = await achievement_crud.get(obj_id=obj_id, session=session)
    return await achievement_crud.remove(db_obj=achievement, session=session)
