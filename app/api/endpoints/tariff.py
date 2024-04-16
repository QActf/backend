from fastapi import APIRouter, Body, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from app.api.validators import check_name_duplicate, check_obj_exists
from app.api_docs_responses.tariff import (CREATE_TARIFF, DELETE_TARIFF,
                                           GET_TARIFF, GET_TARIFFS,
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
    responses=GET_TARIFFS
)
async def get_all_tariffs(
    session: AsyncSession = Depends(get_async_session),
) -> list[TariffRead]:
    """Возвращает все тарифы."""
    return await tariff_crud.get_multi(session)


@router.get(
    '/{tariff_id}',
    response_model=TariffRead,
    responses=GET_TARIFF
)
async def get_tariff(
    tariff_id: Annotated[int, Path(ge=0)],
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает траиф по его id или 404 в случае отсутствия."""
    return await tariff_crud.get(tariff_id, session)


@router.patch(
    '/{tariff_id}',
    response_model=TariffRead,
    dependencies=[Depends(current_superuser)],
    responses=UPDATE_TARIFF
)
async def update_tariff(
    tariff_id: int,
    data: TariffUpdate = Body(
        openapi_examples=REQUEST_NAME_AND_DESCRIPTION_VALUE),
    session: AsyncSession = Depends(get_async_session)
):
    """Обновление тарифa."""
    _tariff = await check_obj_exists(tariff_id, tariff_crud, session)
    return await tariff_crud.update(
        _tariff, data, session
    )


@router.post(
    '/',
    response_model=TariffRead,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED,
    responses=CREATE_TARIFF
)
async def create_tariff(
    tariff: TariffCreate = Body(
        openapi_examples=REQUEST_NAME_AND_DESCRIPTION_VALUE),
    session: AsyncSession = Depends(get_async_session)
):
    """Создать тариф."""
    await check_name_duplicate(tariff.name, tariff_crud, session)
    return await tariff_crud.create(obj_in=tariff, session=session)


@router.delete(
    '/{obj_id}',
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETE_TARIFF
)
async def delete_tariff(
    obj_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить объект."""
    return await delete_obj(obj_id=obj_id, crud=tariff_crud, session=session)
