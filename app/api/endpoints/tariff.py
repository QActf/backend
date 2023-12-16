from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import tariff_crud
from app.schemas.tariff import TarifCreate, TariffRead, TariffCreated


router = APIRouter()


@router.get('/', response_model=list[TariffRead])
async def get_tariffs(
    session: AsyncSession = Depends(get_async_session)
):
    return await tariff_crud.get_multi(session)


@router.post('/', response_model=TariffCreated)
async def create_tariff(
    tariff: TarifCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await tariff_crud.create(tariff, session)
