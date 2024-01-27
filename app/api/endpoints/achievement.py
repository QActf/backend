from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate, check_obj_exists
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import achievement_crud, profile_crud
from app.models import Achievement, User
from app.schemas.achievement import (AchievementCreate, AchievementRead,
                                     AchievementUpdate)
from app.services.endpoints_services import delete_obj

router = APIRouter()


@router.get(
    "/",
    response_model=list[AchievementRead],
    dependencies=[Depends(current_superuser)]
)
async def get_all_achievements(
        session: AsyncSession = Depends(get_async_session),
) -> list[AchievementRead]:
    """Возвращает все achievements."""
    return await achievement_crud.get_multi(session)


@router.get(
    "/me",
    response_model=list[AchievementRead],
    dependencies=[Depends(current_user)]
)
async def get_all_user_achievements(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
) -> list[AchievementRead]:
    """Возвращает все achievements юзера."""
    profile = await profile_crud.get_users_obj(
        user_id=user.id, session=session
    )
    achievements: list[Achievement] = profile.achievements
    return achievements


@router.get(
    "/{achievement_id}",
    response_model=AchievementRead,
    dependencies=[Depends(current_superuser)]
)
async def get_achievement(
        achievement_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> AchievementRead:
    """Возвращает achievement."""
    await check_obj_exists(achievement_id, achievement_crud, session)
    return await achievement_crud.get(obj_id=achievement_id, session=session)


@router.get(
    "/{achievement_id}/me",
    dependencies=[Depends(current_user)]
)
async def get_users_achievement_by_id(
        achievement_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
) -> AchievementRead | dict:
    """Возвращает achievement."""
    await check_obj_exists(achievement_id, achievement_crud, session)
    profile = await profile_crud.get_users_obj(
        user_id=user.id, session=session
    )
    achievement = await achievement_crud.get_users_achievement(
        obj_id=achievement_id, profile=profile
    )
    return achievement


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
    dependencies=[Depends(current_superuser)]
)
async def update_achievement(
        achievement_id: int,
        achievement: AchievementUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    await check_obj_exists(achievement_id, achievement_crud, session)
    _achievement = await achievement_crud.get(
        obj_id=achievement_id, session=session
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
