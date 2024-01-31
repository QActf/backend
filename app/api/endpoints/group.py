from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import group_crud
from app.models import Group, User
from app.schemas.group import GroupCreate, GroupRead, GroupUpdate
from app.services.endpoints_services import delete_obj

from app.services.utils import (Pagination, get_pagination_params, paginated,
                                add_response_headers)

router = APIRouter()


@router.get(
    "/",
    response_model=list[GroupRead],
    dependencies=[Depends(current_superuser)]
)
async def get_all_groups(
    response: Response,
    session: AsyncSession = Depends(get_async_session),
    pagination: Pagination = Depends(get_pagination_params)
) -> list[GroupRead]:
    """Возвращает все группы."""
    groups = await group_crud.get_multi(session)
    response = add_response_headers(
        response, groups, pagination
    )
    return paginated(groups, pagination)


@router.get(
        '/me',
        response_model=list[GroupRead],
        dependencies=[Depends(current_user)]
)
async def get_self_groups(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Получение групп юзером."""
    return await group_crud.get_users_obj(user.id, session)


@router.get(
        '/me/{group_id}',
        response_model=GroupRead,
        dependencies=[Depends(current_user)]
)
async def get_self_group_by_id(
    group_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Получение группы по id юзером."""
    group: Group | None = await group_crud.get(group_id, session)
    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Такой группы не существует.'
        )
    if user not in group.users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Вы не состоите в этой группе.'
        )
    return group


@router.get(
        '/{group_id}',
        response_model=GroupRead,
        dependencies=[Depends(current_superuser)]
)
async def get_group(
    group_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Получение группы по id"""
    return await group_crud.get(group_id, session)


@router.post(
    "/",
    response_model=GroupRead,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED
)
async def create_group(
    group: GroupCreate, session: AsyncSession = Depends(get_async_session)
):
    """Создать группу"""
    await check_name_duplicate(group.name, group_crud, session)
    return await group_crud.create(obj_in=group, session=session)


@router.patch(
        '/{group_id}',
        dependencies=[Depends(current_superuser)],
        response_model=GroupRead
)
async def update_group(
    group_id: int,
    group: GroupUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Апдейт группы."""
    _group = await group_crud.get(group_id, session)
    return await group_crud.update(_group, group, session)


@router.delete(
    "/{obj_id}",
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_group(
    obj_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить объект"""
    return await delete_obj(obj_id=obj_id, crud=group_crud, session=session)
