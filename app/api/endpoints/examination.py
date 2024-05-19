from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate, check_obj_exists
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
    return await check_obj_exists(examination_id, examination_crud, session)


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
    await check_name_duplicate(examination.name, examination_crud, session)
    return await examination_crud.create(
        obj_in=examination, session=session
    )


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
    _examination = await check_obj_exists(
        examination_id, examination_crud, session
    )
    return await examination_crud.update(_examination, data, session)


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
