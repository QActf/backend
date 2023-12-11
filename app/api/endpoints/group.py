from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.group import GroupRead, GroupCreate
from app.core.db import get_async_session
from app.crud import group_crud
from app.api.validators import check_name_duplicate

router = APIRouter()


@router.get('/', response_model=List[GroupRead])
async def get_all_groups(
    session: AsyncSession = Depends(get_async_session)
) -> List[GroupRead]:
    """Возвращает все группы."""
    return await group_crud.get_multi(session)


@router.post('/', response_model=GroupRead)
async def create_group(
    group: GroupCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создать группу"""  # For admin?
    await check_name_duplicate(group.name, group_crud, session)
    group = await group_crud.create(
        obj_in=group, session=session
    )
    session.add(group)
    await session.commit()
    await session.refresh(group)
    return group
