from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import task_crud
from app.schemas.task import TaskCreate, TaskRead


router = APIRouter()


@router.post('/')
async def create_task(
    task: TaskCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await task_crud.create(task, session)


@router.get('/', response_model=list[TaskRead])
async def get_all_tasks(
    session: AsyncSession = Depends(get_async_session)
):
    return await task_crud.get_multi(session)
