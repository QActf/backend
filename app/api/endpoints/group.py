from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import group_crud, user_crud
from app.schemas.group import GroupCreate, GroupRead
from app.models import Group


router = APIRouter()


@router.post('/')
async def create_group(
    group: GroupCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await group_crud.create(group, session=session)


@router.get('/', response_model=List[GroupRead])
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


# @router.post('/{group_id}', response_model=GroupRead)
# async def set_user_in_group(
#     group_id: int,
#     user_id: int,
#     session: AsyncSession = Depends(get_async_session)
# ):
#     user = await user_crud.get(user_id, session=session)
#     group: Group = await group_crud.get(group_id, session=session)
#     group.user.append(user)
#     # TODO