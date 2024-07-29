from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_obj_duplicate, check_obj_exists
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import locale_crud
from app.schemas.locale import (
    LocaleCreate, LocaleCreated, LocaleRead, LocaleReadByID,
)
from tests.test_locale import CREATE_SCHEME

router = APIRouter()


@router.post(
    '/',
    response_model=LocaleCreated,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED
)
async def create_locale(
    locale: LocaleCreate = Body(example=CREATE_SCHEME),
    session: AsyncSession = Depends(get_async_session)
):
    """Создать локаль."""
    obj = await locale_crud.get_by_attr(
        attr_name='language',
        attr_value=locale.language,
        session=session,
    )
    await check_obj_duplicate(obj=obj)
    return await locale_crud.create(locale=locale, session=session)


@router.get(
    '/',
    response_model=list[LocaleRead]
)
async def get_locales(
    session: AsyncSession = Depends(get_async_session)
):
    """Получить список доступных языков."""
    return await locale_crud.get_multi(session)


@router.get(
    '/{locale_id}',
    response_model=LocaleReadByID
)
async def get_locale_by_id(
    locale_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Получение локали по id."""
    obj = await locale_crud.get_by_id(id=locale_id, session=session)
    await check_obj_exists(obj=obj)
    return obj
