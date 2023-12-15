from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.task import TaskRead, TaskCreate
from app.core.db import get_async_session
from app.crud import task_crud
from app.api.validators import check_name_duplicate

router = APIRouter()


@router.get('/', response_model=List[TaskRead])
async def get_all_tasks(
        session: AsyncSession = Depends(get_async_session)
) -> List[TaskRead]:
    """Возвращает все таски."""
    return await task_crud.get_multi(session)


@router.post('/', response_model=TaskRead)
async def create_tariff(
        task: TaskCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Создать таску"""
    await check_name_duplicate(task.name, task_crud, session)
    task = await task_crud.create(
        obj_in=task, session=session
    )
    return task


@router.delete('/')
async def delete_task(
        obj_id: str,
        session: AsyncSession = Depends(get_async_session),
):
    """Удалить объект"""
    task = await task_crud.get(obj_id=obj_id, session=session)
    return await task_crud.remove(db_obj=task, session=session)
