from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.contact_information_block import contact_info_crud
from app.schemas.contact_information_block import (
    ContactInformationBlockCreate, ContactInformationBlockRead,
    ContactInformationBlockUpdate
)


router = APIRouter()


@router.post('/')
async def create_contact_info(
    contact_block: ContactInformationBlockCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await contact_info_crud.create(contact_block, session)


@router.get(
    '/',
    response_model=ContactInformationBlockRead,
)
async def get_contact_block(
    session: AsyncSession = Depends(get_async_session)
):
    contact_info = await contact_info_crud.get_contact_info(session)
    if contact_info:
        return contact_info
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Контактные данные еще не созданы.'
    )


@router.patch(
    '/',
    response_model=ContactInformationBlockRead
)
async def update_contact_info(
    new_info: ContactInformationBlockUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    contact_info = await contact_info_crud.get_contact_info(session)
    if contact_info is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Контактные данные еще не созданы.'
        )
    return await contact_info_crud.update(
        contact_info,
        new_info,
        session
    )
