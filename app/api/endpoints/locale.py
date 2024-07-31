from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_obj_duplicate, check_obj_exists
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import locale_crud
from app.schemas.locale import (
    LocaleCreate, LocaleCreated, LocaleRead, LocaleReadByID, LocaleReadByLang,
)
from tests.test_locale import CREATE_SCHEMA

router = APIRouter()


@router.post(
    '/',
    response_model=LocaleCreated,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED
)
async def create_locale(
    locale: LocaleCreate = Body(example=CREATE_SCHEMA),
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
    response_model=LocaleReadByID,
)
async def get_locale_by_id(
    locale_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Получение локали по id."""
    obj = await locale_crud.get_by_attr(
        attr_name='id',
        attr_value=locale_id,
        session=session,
    )
    await check_obj_exists(obj=obj)
    return obj


@router.get(
    '/lang/{locale_language}',
    response_model=LocaleReadByLang,
)
async def get_locale_by_language(
    locale_language: str,
    session: AsyncSession = Depends(get_async_session)
):
    """Получение локали по language."""
    obj = await locale_crud.get_by_attr(
        attr_name='language',
        attr_value=locale_language,
        session=session,
    )
    await check_obj_exists(obj=obj)
    return obj


@router.put(
    '/',
    response_model=LocaleCreated,
    dependencies=[Depends(current_superuser)],
)
async def update_or_create_locale(
    locale: LocaleCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Обновит или создаст локаль."""
    obj = await locale_crud.get_by_attr(
        attr_name='language',
        attr_value=locale.language,
        session=session,
    )
    if obj:
        return await locale_crud.update(
            db_obj=obj,
            obj_in=locale,
            session=session,
        )
    return await locale_crud.create(locale=locale, session=session)


@router.delete(
    '/lang/{locale_language}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(current_superuser)],
)
async def delete_locale(
    locale_language: str,
    session: AsyncSession = Depends(get_async_session)
):
    """Удалит локаль по language."""
    obj = await locale_crud.get_by_attr(
        attr_name='language',
        attr_value=locale_language,
        session=session,
    )
    await check_obj_exists(obj=obj)
    await locale_crud.remove(db_obj=obj, session=session)
