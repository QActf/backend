from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate, check_obj_exists
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import examination_crud
from app.schemas.examination import (ExaminationCreate, ExaminationRead,
                                     ExaminationUpdate)
from app.services.endpoints_services import delete_obj
from app.models import User

router = APIRouter()


@router.get(
    "/",
    response_model=list[ExaminationRead],
)
async def get_all_examinations(
    session: AsyncSession = Depends(get_async_session),
) -> list[ExaminationRead]:
    """Возвращает все Examination."""
    return await examination_crud.get_multi(session)


@router.get(
        '/me',
        response_model=list[ExaminationRead],
        dependencies=[Depends(current_user)]
)
async def get_self_examinations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Получение групп юзером."""
    return await examination_crud.get_users_obj(user.id, session)


@router.get(
        '/{examination_id}',
        response_model=ExaminationRead
)
async def get_examination(
    examination_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает экзаминейшн по id."""
    return await check_obj_exists(examination_id, examination_crud, session)


@router.post(
    "/",
    response_model=ExaminationRead,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED
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
        '/{examination_id}',
        dependencies=[Depends(current_superuser)],
        response_model=ExaminationRead
)
async def update_group(
    examination_id: int,
    data: ExaminationUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Апдейт examination."""
    _examination = await check_obj_exists(
        examination_id, examination_crud, session
    )
    return await examination_crud.update(_examination, data, session)


@router.delete(
    "/{obj_id}",
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_examination(
    obj_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить объект"""
    return await delete_obj(
        obj_id=obj_id, crud=examination_crud, session=session
    )
