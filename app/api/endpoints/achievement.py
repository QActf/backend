from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import achievement_crud
from app.schemas.achievement import (AchievementCreate, AchievementRead,
                                     AchievementUpdate)
from app.services.endpoints_services import delete_obj, get_obj

router = APIRouter()


@router.get(
    "/",
    response_model=list[AchievementRead],
    dependencies=[Depends(current_user)]
)
async def get_all_achievements(
        session: AsyncSession = Depends(get_async_session),
) -> list[AchievementRead]:
    """Возвращает все achievements."""
    return await achievement_crud.get_multi(session)


@router.get(
    "/{achievement_id}",
    response_model=AchievementRead,
    dependencies=[Depends(current_user)]
)
async def get_achievement(
        achievement_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> AchievementRead:
    """Возвращает achievement."""
    return await get_obj(
        obj_id=achievement_id, crud=achievement_crud, session=session
    )


@router.post(
    "/",
    response_model=AchievementRead,
    dependencies=[Depends(current_superuser)]
)
async def create_achievement(
        achievement: AchievementCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Создать Achievement"""
    await check_name_duplicate(achievement.name, achievement_crud, session)
    return await achievement_crud.create(obj_in=achievement, session=session)


@router.patch(
    "/{achievement_id}",
    response_model=AchievementRead,
    dependencies=[Depends(current_user)]
)
async def update_achievement(
        achievement_id: int,
        achievement: AchievementUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    _achievement = await get_obj(
        obj_id=achievement_id, crud=achievement_crud, session=session
    )
    return await achievement_crud.update(_achievement, achievement, session)


@router.delete("/{obj_id}", dependencies=[Depends(current_superuser)])
async def delete_achievement(
        obj_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Удалить объект"""
    return await delete_obj(
        obj_id=obj_id, crud=achievement_crud, session=session
    )
