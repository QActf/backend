from typing import List

from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate
from app.api_docs_responses.task import (CREATE_TASK, DELETE_TASK, GET_TASK,
                                         GET_TASKS)
from app.api_docs_responses.utils_docs import \
    REQUEST_NAME_AND_DESCRIPTION_VALUE
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import task_crud
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.endpoints_services import delete_obj

router = APIRouter()


@router.get(
    "/",
    response_model=List[TaskRead],
    dependencies=[Depends(current_superuser)],
    responses=GET_TASKS
)
async def get_all_tasks(
    session: AsyncSession = Depends(get_async_session),
) -> List[TaskRead]:
    """Возвращает все задачи."""
    return await task_crud.get_multi(session)


@router.get(
    '/{task_id}',
    response_model=TaskRead,
    dependencies=[Depends(current_superuser)],
    responses=GET_TASK
)
async def get_task_by_id(
    task_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Получение задачи по id."""
    return await task_crud.get(task_id, session)


@router.post(
    "/",
    response_model=TaskRead,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED,
    responses=CREATE_TASK
)
async def create_task(
    task: TaskCreate = Body(
        openapi_examples=REQUEST_NAME_AND_DESCRIPTION_VALUE),
    session: AsyncSession = Depends(get_async_session)
):
    """Создать задачу"""
    await check_name_duplicate(task.name, task_crud, session)
    return await task_crud.create(obj_in=task, session=session)


@router.patch(
    '/{task_id}',
    response_model=TaskRead,
    dependencies=[Depends(current_superuser)],
    responses=GET_TASK
)
async def update_task(
    task_id: int,
    data: TaskUpdate = Body(
        openapi_examples=REQUEST_NAME_AND_DESCRIPTION_VALUE),
    session: AsyncSession = Depends(get_async_session)
):
    """Обновление задачи."""
    _task = await task_crud.get(task_id, session)
    return await task_crud.update(_task, data, session)


@router.delete(
    "/{obj_id}",
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETE_TASK
)
async def delete_task(
    obj_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить задачу"""
    return await delete_obj(obj_id=obj_id, crud=task_crud, session=session)
