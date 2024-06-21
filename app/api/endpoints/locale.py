from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.locale import (
    LocaleCreate, LocaleReadByID,
    LocaleRead, LocaleCreated
)
from app.crud import locale_crud


router = APIRouter()


@router.post(
    '/',
    response_model=LocaleCreated,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED
)
async def create_locale(
    locale: LocaleCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создать локаль."""
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
    return await locale_crud.get_by_id(locale_id, session)
