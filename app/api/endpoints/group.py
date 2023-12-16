from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.core.db import get_async_session
from app.crud import group_crud
from app.schemas.group import GroupCreate, GroupRead, GroupRemove


router = APIRouter()


@router.post('/')
async def create_group(
    group: GroupCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await group_crud.create(group, session=session)


@router.get('/', response_model=list[GroupRead])
async def get_all_groups(
    session: AsyncSession = Depends(get_async_session)
):
    return await group_crud.get_multi(session=session)


@router.get('/{group_id}', response_model=GroupRead)
async def get_group(
        group_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await group_crud.get(group_id, session=session)


@router.delete('/{group_id}')
async def delete_group(
    group_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        db_obj = await group_crud.get(group_id, session)
        return await group_crud.remove(db_obj, session)
    except UnmappedInstanceError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Группа с id {group_id} не найдена.'
        )
