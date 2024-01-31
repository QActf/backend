from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import achievement_crud
from app.models import Achievement, User
from app.schemas.achievement import (AchievementCreate, AchievementRead,
                                     AchievementUpdate)
from app.services.endpoints_services import delete_obj
from app.services.utils import (Pagination, add_response_headers,
                                get_pagination_params, paginated)

router = APIRouter()


@router.get(
    "/",
    response_model=list[AchievementRead],
    dependencies=[Depends(current_superuser)]
)
async def get_all_achievements(
    response: Response,
    pagination: Pagination = Depends(get_pagination_params),
    session: AsyncSession = Depends(get_async_session),
) -> list[AchievementRead]:
    """Возвращает все achievement."""
    achievements = await achievement_crud.get_multi(session)
    response = add_response_headers(
        response, achievements, pagination
    )
    return paginated(achievements, pagination)


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


@router.get(
        '/me/{achievement_id}',
        response_model=AchievementRead,
        dependencies=[Depends(current_user)]
)
async def get_self_achievement_by_id(
    achievement_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает ачивмент юзера по id."""
    achievement: Achievement = await achievement_crud.get(
        achievement_id, session
    )
    if achievement is None:
        raise HTTPException(
            status_code=404,
            detail='Achievement не существует.'
        )
    if user.id not in [_.id for _ in achievement.profiles]:
        raise HTTPException(
            status_code=403,
            detail='У выс нет этого achievement.'
        )
    return achievement


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


@router.patch(
        '/{achievement_id}',
        response_model=AchievementRead,
        dependencies=[Depends(current_superuser)]
)
async def update_achievement(
    achievement_id: int,
    data: AchievementUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Апдейт ачивмент."""
    _achievement = await achievement_crud.get(achievement_id, session)
    return await achievement_crud.update(
        _achievement, data, session
    )


@router.delete("/{obj_id}", dependencies=[Depends(current_superuser)],
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_achievement(
    obj_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить объект"""
    return await delete_obj(
        obj_id=obj_id, crud=achievement_crud, session=session
    )
