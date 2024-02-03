from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate, check_obj_exists
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import examination_crud, user_crud
from app.models import Examination, User
from app.schemas.examination import (ExaminationCreate, ExaminationRead,
                                     ExaminationUpdate)
from app.services.endpoints_services import delete_obj

router = APIRouter()


@router.get(
    "/",
    response_model=list[ExaminationRead],
    dependencies=[Depends(current_superuser)]
)
async def get_all_examinations(
    session: AsyncSession = Depends(get_async_session),
) -> list[ExaminationRead]:
    """Возвращает все Examination."""
    return await examination_crud.get_multi(session)


@router.get(
    "/me",
    response_model=list[ExaminationRead],
    dependencies=[Depends(current_user)]
)
async def get_all_user_examinations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
) -> list[ExaminationRead]:
    """Возвращает все Examination юзера."""
    user = await user_crud.get(user.id, session)
    achievements: list[Examination] = user.examinations
    return achievements


@router.get(
    "/{examination_id}",
    response_model=ExaminationRead,
    dependencies=[Depends(current_superuser)]
)
async def get_examination(
        examination_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> ExaminationRead:
    """Возвращает examination."""
    await check_obj_exists(examination_id, examination_crud, session)
    return await examination_crud.get(examination_id, session=session)


@router.get(
    "/{achievement_id}/me",
    dependencies=[Depends(current_user)]
)
async def get_users_achievement_by_id(
        achievement_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
) -> ExaminationRead | dict:
    """Возвращает achievement."""
    await check_obj_exists(achievement_id, examination_crud, session)
    user = await user_crud.get(user.id, session)
    examination = await examination_crud.get_users_examination(
        obj_id=achievement_id, user=user
    )
    return examination


@router.post(
    "/",
    response_model=ExaminationRead,
    dependencies=[Depends(current_superuser)]
)
async def create_examination(
    examination: ExaminationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создать Examination"""
    await check_name_duplicate(examination.name, examination_crud, session)
    return await examination_crud.create(
        obj_in=examination, session=session
    )


@router.patch(
    "/{examination_id}",
    response_model=ExaminationRead,
    dependencies=[Depends(current_superuser)]
)
async def update_examination(
        examination_id: int,
        examination: ExaminationUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """Обновляет Examination"""
    await check_obj_exists(examination_id, examination_crud, session)
    _examination = await examination_crud.get(examination_id, session=session)
    return await examination_crud.update(_examination, examination, session)


@router.delete(
    "/{obj_id}",
    dependencies=[Depends(current_superuser)]
)
async def delete_examination(
    obj_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить объект"""
    return await delete_obj(
        obj_id=obj_id, crud=examination_crud, session=session
    )
