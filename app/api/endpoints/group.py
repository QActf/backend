from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import group_crud
from app.schemas.group import GroupCreate, GroupRead
from app.services.endpoints_services import delete_obj

router = APIRouter()


@router.get(
    "/",
    response_model=list[GroupRead],
    dependencies=[Depends(current_user)]
)
async def get_all_groups(
    session: AsyncSession = Depends(get_async_session),
) -> list[GroupRead]:
    """Возвращает все группы."""
    return await group_crud.get_multi(session)


@router.get(
        '/{group_id}',
        response_model=GroupRead,
        dependencies=[Depends(current_superuser)]
)
async def get_group(
    session: AsyncSession = Depends(get_async_session)
):
    """Получение группы по id"""
    ...


@router.post(
    "/",
    response_model=GroupRead,
    dependencies=[Depends(current_superuser)],
    status_code=201
)
async def create_group(
    group: GroupCreate, session: AsyncSession = Depends(get_async_session)
):
    """Создать группу"""
    await check_name_duplicate(group.name, group_crud, session)
    return await group_crud.create(obj_in=group, session=session)


@router.delete(
    "/{obj_id}",
    dependencies=[Depends(current_superuser)]
)
async def delete_group(
    obj_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить объект"""
    return await delete_obj(obj_id=obj_id, crud=group_crud, session=session)
