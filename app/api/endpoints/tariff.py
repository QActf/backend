from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user import current_user
from app.models import User
from app.schemas.tariff import TariffRead, TariffCreate
from app.schemas.user import UserRead
from app.core.db import get_async_session
from app.crud import tariff_crud, user_crud
from app.api.validators import check_name_duplicate, check_obj_exists
from app.services.endpoints_services import delete_obj

router = APIRouter()


@router.get('/', response_model=list[TariffRead])
async def get_all_tariffs(
        session: AsyncSession = Depends(get_async_session)
) -> list[TariffRead]:
    """Возвращает все тарифы."""
    return await tariff_crud.get_multi(session)


@router.put('/', response_model=UserRead)
async def update_users_tariff(
        tariff_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> UserRead:
    """Привязывает тариф к юзеру"""
    await check_obj_exists(tariff_id, tariff_crud, session)
    user = await user_crud.update_id(
        session=session, db_obj=user, field='tariff_id', field_value=tariff_id
    )
    return user


@router.post('/', response_model=TariffRead)
async def create_tariff(
        tariff: TariffCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Создать Тариф"""
    await check_name_duplicate(tariff.name, tariff_crud, session)
    return await tariff_crud.create(
        obj_in=tariff, session=session
    )


@router.delete('/{obj_id}')
async def delete_tariff(
        obj_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Удалить объект"""
    return await delete_obj(obj_id=obj_id, crud=tariff_crud, session=session)
