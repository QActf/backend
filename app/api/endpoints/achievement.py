from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate
from app.schemas.achievement import AchievementRead, AchievementCreate
from app.core.db import get_async_session
from app.crud import achievement_crud
from app.services.endpoints_services import delete_obj

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
    return await delete_obj(obj_id=obj_id, crud=achievement_crud, session=session)
