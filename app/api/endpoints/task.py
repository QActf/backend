from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import task_crud
from app.schemas.task import TaskCreate, TaskRead
from app.services.endpoints_services import delete_obj

router = APIRouter()


@router.get(
    "/",
    response_model=List[TaskRead],
    dependencies=[Depends(current_user)]
)
async def get_all_tasks(
    session: AsyncSession = Depends(get_async_session),
) -> List[TaskRead]:
    """Возвращает все таски."""
    return await task_crud.get_multi(session)


@router.post(
    "/",
    response_model=TaskRead,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED
)
async def create_task(
    task: TaskCreate, session: AsyncSession = Depends(get_async_session)
):
    """Создать таску"""
    await check_name_duplicate(task.name, task_crud, session)
    return await task_crud.create(obj_in=task, session=session)


@router.delete("/{obj_id}", dependencies=[Depends(current_superuser)])
async def delete_task(
    obj_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить объект"""
    return await delete_obj(obj_id=obj_id, crud=task_crud, session=session)
