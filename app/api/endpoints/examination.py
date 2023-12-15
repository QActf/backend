from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate
from app.schemas.examination import ExaminationRead, ExaminationCreate
from app.core.db import get_async_session
from app.crud import examination_crud

router = APIRouter()


@router.get('/', response_model=List[ExaminationRead])
async def get_all_examinations(
        session: AsyncSession = Depends(get_async_session)
) -> List[ExaminationRead]:
    """Возвращает все Examination."""
    return await examination_crud.get_multi(session)


@router.post('/', response_model=ExaminationRead)
async def create_examination(
        examination: ExaminationCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Создать Examination"""
    await check_name_duplicate(examination.name, examination_crud, session)
    examination = await examination_crud.create(
        obj_in=examination, session=session
    )
    return examination


@router.delete('/')
async def delete_examination(
        obj_id: str,
        session: AsyncSession = Depends(get_async_session),
):
    """Удалить объект"""
    examination = await examination_crud.get(obj_id=obj_id, session=session)
    return await examination_crud.remove(db_obj=examination, session=session)
