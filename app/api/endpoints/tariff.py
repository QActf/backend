from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate, check_obj_exists
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import tariff_crud
from app.schemas.tariff import TariffCreate, TariffRead, TariffUpdate
from app.services.endpoints_services import delete_obj

router = APIRouter()


@router.get(
    "/",
    response_model=list[TariffRead],
)
async def get_all_tariffs(
    session: AsyncSession = Depends(get_async_session),
) -> list[TariffRead]:
    """Возвращает все тарифы."""
    return await tariff_crud.get_multi(session)


@router.get(
        '/{tariff_id}',
        response_model=TariffRead
)
async def get_tariff(
    tariff_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    return await tariff_crud.get(tariff_id, session)


@router.patch(
        '/{tariff_id}',
        response_model=TariffRead,
        dependencies=[Depends(current_superuser)]
)
async def update_tariff(
    tariff_id: int,
    data: TariffUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Апдейт тарифа."""
    _tariff = await check_obj_exists(tariff_id, tariff_crud, session)
    return await tariff_crud.update(
        _tariff, data, session
    )


# Перенести в эндпоинты юзера?
# @router.patch(
#     "/{tariff_id}",
#     response_model=UserRead,
#     dependencies=[Depends(current_user)]
# )
# async def update_users_tariff(
#     tariff_id: int,
#     user: User = Depends(current_user),
#     session: AsyncSession = Depends(get_async_session),
# ) -> UserRead:
#     """Привязывает тариф к юзеру"""
#     await check_obj_exists(tariff_id, tariff_crud, session)
#     user = await user_crud.update_id(
#         session=session, db_obj=user, field="tariff_id",
#         field_value=tariff_id
#     )
#     return user


@router.post(
    "/",
    response_model=TariffRead,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED
)
async def create_tariff(
    tariff: TariffCreate, session: AsyncSession = Depends(get_async_session)
):
    """Создать Тариф"""
    await check_name_duplicate(tariff.name, tariff_crud, session)
    return await tariff_crud.create(obj_in=tariff, session=session)


@router.delete(
    "/{obj_id}",
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_tariff(
    obj_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить объект"""
    return await delete_obj(obj_id=obj_id, crud=tariff_crud, session=session)
