from fastapi import APIRouter, Body, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from app.api.validators import check_name_duplicate, check_obj_exists
from app.api_docs_responses.tariff import (ALL_TARIFFS_DECRIPTION,
                                           CREATE_TARIFF, DELETE_TARIFF,
                                           GET_TARIFF, GET_TARIFFS,
                                           TARIFF_CREATE_DESCRIPTION,
                                           TARIFF_ID_DELETE,
                                           TARIFF_ID_DESCRIPTION,
                                           TARIFF_ID_PATCH_ODESCRIPTION,
                                           UPDATE_TARIFF)
from app.api_docs_responses.utils_docs import \
    REQUEST_NAME_AND_DESCRIPTION_VALUE
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import tariff_crud
from app.schemas.tariff import TariffCreate, TariffRead, TariffUpdate
from app.services.endpoints_services import delete_obj

router = APIRouter()


@router.get(
    '/',
    response_model=list[TariffRead],
    responses=GET_TARIFFS,
    summary='Получение всех тарифов.',
    description=ALL_TARIFFS_DECRIPTION,
)
async def get_all_tariffs(
    session: AsyncSession = Depends(get_async_session),
) -> list[TariffRead]:
    """
    Получение всех тарифов, который есть в БД.
    """
    return await tariff_crud.get_multi(session)


@router.get(
    '/{tariff_id}',
    response_model=TariffRead,
    responses=GET_TARIFF,
    summary='Получение тарифа по id.',
    description=TARIFF_ID_DESCRIPTION,
)
async def get_tariff(
    tariff_id: Annotated[int, Path(ge=0)],
    session: AsyncSession = Depends(get_async_session)
):
    """
    Получение тарифа по его id или
    получение ошибки 404 в случае отсутствия данного тарифа.
    """
    return await tariff_crud.get(tariff_id, session)


@router.patch(
    '/{tariff_id}',
    response_model=TariffRead,
    dependencies=[Depends(current_superuser)],
    responses=UPDATE_TARIFF,
    summary='Обновление тарифа по id.',
    description=TARIFF_ID_PATCH_ODESCRIPTION,
)
async def update_tariff(
    tariff_id: int,
    data: TariffUpdate = Body(
        openapi_examples=REQUEST_NAME_AND_DESCRIPTION_VALUE),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Частичное обновление информации о тарифе по его идентификатору.
    """
    _tariff = await check_obj_exists(tariff_id, tariff_crud, session)
    return await tariff_crud.update(
        _tariff, data, session
    )


@router.post(
    '/',
    response_model=TariffRead,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED,
    responses=CREATE_TARIFF,
    summary='Создание тарифа.',
    description=TARIFF_CREATE_DESCRIPTION,
)
async def create_tariff(
    tariff: TariffCreate = Body(
        openapi_examples=REQUEST_NAME_AND_DESCRIPTION_VALUE),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Создание тарифа.
    """
    await check_name_duplicate(tariff.name, tariff_crud, session)
    return await tariff_crud.create(obj_in=tariff, session=session)


@router.delete(
    '/{tariff_id}',
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETE_TARIFF,
    summary='Удаление тарфиа по id.',
    description=TARIFF_ID_DELETE,
)
async def delete_tariff(
    tariff_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Удаление тарифа по его идентификатору.
    """
    return await delete_obj(
        obj_id=tariff_id,
        crud=tariff_crud,
        session=session,
    )
