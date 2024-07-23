from typing import List

from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_obj_duplicate, check_obj_exists
from app.api_docs_responses.task import (
    CREATE_TASK, DELETE_TASK, GET_TASK, GET_TASKS, PATCH_TASK,
)
from app.api_docs_responses.utils_docs import (
    REQUEST_NAME_AND_DESCRIPTION_VALUE,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import task_crud
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.endpoints_services import delete_obj

router = APIRouter()


@router.get(
    '/',
    response_model=List[TaskRead],
    dependencies=[Depends(current_superuser)],
    **GET_TASKS,
)
async def get_all_tasks(
    session: AsyncSession = Depends(get_async_session),
) -> List[TaskRead]:
    """Возвращает все задачи."""
    return await task_crud.get_multi(session=session)


@router.get(
    '/{task_id}',
    response_model=TaskRead,
    dependencies=[Depends(current_superuser)],
    **GET_TASK,
)
async def get_task_by_id(
    task_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Получение задачи по id."""
    obj = await task_crud.get_by_attr(
        attr_name='id',
        attr_value=task_id,
        session=session,
    )
    await check_obj_exists(obj=obj)
    return obj


@router.post(
    '/',
    response_model=TaskRead,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED,
    **CREATE_TASK,
)
async def create_task(
    task: TaskCreate = Body(
        openapi_examples=REQUEST_NAME_AND_DESCRIPTION_VALUE),
    session: AsyncSession = Depends(get_async_session)
):
    """Создать задачу"""
    obj = await task_crud.get_by_attr(
        attr_name='name',
        attr_value=task.name,
        session=session,
    )
    await check_obj_duplicate(obj=obj)
    return await task_crud.create(obj_in=task, session=session)


@router.patch(
    '/{task_id}',
    response_model=TaskRead,
    dependencies=[Depends(current_superuser)],
    **PATCH_TASK,
)
async def update_task(
    task_id: int,
    data: TaskUpdate = Body(
        openapi_examples=REQUEST_NAME_AND_DESCRIPTION_VALUE),
    session: AsyncSession = Depends(get_async_session)
):
    """Обновление задачи."""
    obj = await task_crud.get_by_attr(
        attr_name='id',
        attr_value=task_id,
        session=session,
    )
    await check_obj_exists(obj=obj)
    return await task_crud.update(db_obj=obj, obj_in=data, session=session)


@router.delete(
    '/{task_id}',
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_204_NO_CONTENT,
    **DELETE_TASK,
)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить задачу"""
    return await delete_obj(obj_id=task_id, crud=task_crud, session=session)
