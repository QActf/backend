from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate, check_obj_exists
from app.api_docs_responses.achievement import (CREATE_ACHIEVEMENT,
                                                DELETE_ACHIEVEMENT,
                                                GET_ACHIEVEMENT,
                                                GET_ACHIEVEMENTS,
                                                GET_ME_ACHIEVEMENT)
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
    dependencies=[Depends(current_superuser)],
    responses=GET_ACHIEVEMENTS
)
async def get_all_achievements(
    response: Response,
    pagination: Pagination = Depends(get_pagination_params),
    session: AsyncSession = Depends(get_async_session),
) -> list[AchievementRead]:
    """Возвращает все достижения."""
    achievements = await achievement_crud.get_multi(session)
    add_response_headers(
        response, achievements, pagination
    )
    return paginated(achievements, pagination)


@router.get(
    '/me',
    response_model=list[AchievementRead],
    dependencies=[Depends(current_user)],
    responses=GET_ACHIEVEMENTS
)
async def get_self_achievements(
    response: Response,
    pagination: Pagination = Depends(get_pagination_params),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает достижения текущего пользователя."""
    achievements = await achievement_crud.get_users_obj(user.id, session)
    add_response_headers(
        response, achievements, pagination
    )
    return paginated(achievements, pagination)


@router.get(
    '/me/{achievement_id}',
    response_model=AchievementRead,
    dependencies=[Depends(current_user)],
    responses=GET_ME_ACHIEVEMENT
)
async def get_self_achievement_by_id(
    achievement_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает достижение текущего пользователя по id."""
    achievement: Achievement = await achievement_crud.get(
        achievement_id, session
    )
    if achievement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Достижение не существует.'
        )
    if user.id not in [_.id for _ in achievement.profiles]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='У вас нет этого достижения.'
        )
    return achievement


@router.post(
    "/",
    response_model=AchievementRead,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED,
    responses=CREATE_ACHIEVEMENT
)
async def create_achievement(
    achievement: AchievementCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создать достижение"""
    await check_name_duplicate(achievement.name, achievement_crud, session)
    return await achievement_crud.create(obj_in=achievement, session=session)


@router.patch(
    '/{achievement_id}',
    response_model=AchievementRead,
    dependencies=[Depends(current_superuser)],
    responses=GET_ACHIEVEMENT
)
async def update_achievement(
    achievement_id: int,
    data: AchievementUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Обновить достижение."""
    _achievement = await check_obj_exists(
        achievement_id,
        achievement_crud,
        session
    )
    return await achievement_crud.update(
        _achievement, data, session
    )


@router.delete(
    "/{obj_id}",
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETE_ACHIEVEMENT
)
async def delete_achievement(
    obj_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить достижение."""
    return await delete_obj(
        obj_id=obj_id, crud=achievement_crud, session=session
    )
