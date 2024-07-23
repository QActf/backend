from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_obj_duplicate, check_obj_exists
from app.api_docs_responses.group import (
    CREATE_GROUP, DELETE_GROUP, GET_GROUP, GET_GROUPS, GET_USER_GROUP,
)
from app.api_docs_responses.utils_docs import (
    REQUEST_NAME_AND_DESCRIPTION_VALUE,
)
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import group_crud
from app.models import Group, User
from app.schemas.group import GroupCreate, GroupRead, GroupUpdate
from app.services.endpoints_services import delete_obj
from app.services.utils import (
    Pagination, add_response_headers, get_pagination_params, paginated,
)

router = APIRouter()


@router.get(
    '/',
    response_model=list[GroupRead],
    dependencies=[Depends(current_superuser)],
    responses=GET_GROUPS,
    response_model_exclude_none=True
)
async def get_all_groups(
    response: Response,
    session: AsyncSession = Depends(get_async_session),
    pagination: Pagination = Depends(get_pagination_params)
) -> list[GroupRead]:
    """Возвращает все группы."""
    groups = await group_crud.get_multi(session)
    add_response_headers(response, groups, pagination)
    return paginated(groups, pagination)


@router.get(
    '/me',
    response_model=list[GroupRead],
    dependencies=[Depends(current_user)],
    responses=GET_GROUPS
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
    dependencies=[Depends(current_user)],
    responses=GET_USER_GROUP
)
async def get_self_group_by_id(
    group_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Получение группы по id юзером."""
    obj: Group | None = await group_crud.get(group_id, session)
    await check_obj_exists(obj=obj)

    if user not in obj.users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Вы не состоите в этой группе.'
        )
    return obj


@router.get(
    '/{group_id}',
    response_model=GroupRead,
    dependencies=[Depends(current_superuser)],
    responses=GET_GROUP
)
async def get_group(
    group_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Получение группы по id"""
    obj = await group_crud.get(group_id, session)
    await check_obj_exists(obj=obj)
    return obj


@router.post(
    '/',
    response_model=GroupRead,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED,
    responses=CREATE_GROUP
)
async def create_group(
    group: GroupCreate = Body(
        openapi_examples=REQUEST_NAME_AND_DESCRIPTION_VALUE),
    session: AsyncSession = Depends(get_async_session)
):
    """Создать группу"""
    obj = await group_crud.get_by_attr(
        attr_name='name',
        attr_value=group.name,
        session=session,
    )
    await check_obj_duplicate(obj=obj)
    return await group_crud.create(obj_in=group, session=session)


@router.patch(
    '/{group_id}',
    dependencies=[Depends(current_superuser)],
    response_model=GroupRead,
    responses=GET_GROUP
)
async def update_group(
    group_id: int,
    group: GroupUpdate = Body(
        openapi_examples=REQUEST_NAME_AND_DESCRIPTION_VALUE),
    session: AsyncSession = Depends(get_async_session)
):
    """Обновить группу"""
    obj = await group_crud.get(group_id=group_id, session=session)
    await check_obj_exists(obj=obj)
    return await group_crud.update(db_obj=obj, obj_in=group, session=session)


@router.delete(
    '/{obj_id}',
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETE_GROUP
)
async def delete_group(
    obj_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить группу"""
    return await delete_obj(obj_id=obj_id, crud=group_crud, session=session)
