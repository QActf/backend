from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import achievement_crud
from app.schemas.achievement import AchievementCreate, AchievementRead
from app.services.endpoints_services import delete_obj
from app.models import User

router = APIRouter()


@router.get(
    "/",
    response_model=list[AchievementRead],
    dependencies=[Depends(current_superuser)]
)
async def get_all_achievements(
    session: AsyncSession = Depends(get_async_session),
) -> list[AchievementRead]:
    """Возвращает все achievement."""
    return await achievement_crud.get_multi(session)


@router.get(
        '/me',
        response_model=list[AchievementRead],
        dependencies=[Depends(current_user)]
)
async def get_self_achievements(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает ачивментс юзера."""
    return await achievement_crud.get_users_obj(user.id, session)


@router.post(
    "/",
    response_model=AchievementRead,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED
)
async def create_achievement(
    achievement: AchievementCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создать Achievement"""
    await check_name_duplicate(achievement.name, achievement_crud, session)
    return await achievement_crud.create(obj_in=achievement, session=session)


@router.delete("/{obj_id}", dependencies=[Depends(current_superuser)])
async def delete_achievement(
    obj_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить объект"""
    return await delete_obj(
        obj_id=obj_id, crud=achievement_crud, session=session
    )
