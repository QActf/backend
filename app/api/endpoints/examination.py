from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_obj_duplicate, check_obj_exists
from app.api_docs_responses.examination import (
    CREATE_EXAMINATION, DELETE_EXAMINATION, GET_EXAMINATION, GET_EXAMINATIONS,
    GET_USER_EXAMINATIONS, UPDATE_EXAMINATION,
)
from app.api_docs_responses.utils_docs import (
    REQUEST_NAME_AND_DESCRIPTION_VALUE,
)
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import examination_crud
from app.models import User
from app.schemas.examination import (
    ExaminationCreate, ExaminationRead, ExaminationUpdate,
)
from app.services.endpoints_services import delete_obj

router = APIRouter()


@router.get(
    '/',
    response_model=list[ExaminationRead],
    **GET_EXAMINATIONS,
)
async def get_all_examinations(
    session: AsyncSession = Depends(get_async_session),
) -> list[ExaminationRead]:
    """Возвращает все экзамены."""
    return await examination_crud.get_multi(session)


@router.get(
    '/me',
    response_model=list[ExaminationRead],
    dependencies=[Depends(current_user)],
    **GET_USER_EXAMINATIONS,
)
async def get_self_examinations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает экзамены текущего пользователя."""
    return await examination_crud.get_users_obj(user.id, session)


@router.get(
    '/{examination_id}',
    response_model=ExaminationRead,
    dependencies=[Depends(current_user)],
    **GET_EXAMINATION,
)
async def get_examination(
    examination_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает экзамен по id."""
    obj = await examination_crud.get_by_attr(
        attr_name='id',
        attr_value=examination_id,
        session=session,
    )
    await check_obj_exists(obj=obj)
    return obj


@router.post(
    '/',
    response_model=ExaminationRead,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED,
    **CREATE_EXAMINATION,
)
async def create_examination(
    examination: ExaminationCreate = Body(
        openapi_examples=REQUEST_NAME_AND_DESCRIPTION_VALUE),
    session: AsyncSession = Depends(get_async_session)
):
    """Создать экзамен."""
    obj = await examination_crud.get_by_attr(
        attr_name='name',
        attr_value=examination.name,
        session=session,
    )
    await check_obj_duplicate(obj)
    return await examination_crud.create(obj_in=examination, session=session)


@router.patch(
    '/{examination_id}',
    dependencies=[Depends(current_superuser)],
    response_model=ExaminationRead,
    **UPDATE_EXAMINATION,
)
async def update_examination(
    examination_id: int,
    data: ExaminationUpdate = Body(
        openapi_examples=REQUEST_NAME_AND_DESCRIPTION_VALUE),
    session: AsyncSession = Depends(get_async_session)
):
    """Обновить экзамен."""
    obj = await examination_crud.get_by_attr(
        attr_name='id',
        attr_value=examination_id,
        session=session,
    )
    await check_obj_exists(obj=obj)
    return await examination_crud.update(
        db_obj=obj,
        obj_in=data,
        session=session,
    )


@router.delete(
    '/{examination_id}',
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_204_NO_CONTENT,
    **DELETE_EXAMINATION
)
async def delete_examination(
    examination_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Удалить экзамен."""
    return await delete_obj(
        obj_id=examination_id, crud=examination_crud, session=session
    )
