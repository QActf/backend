from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import examination_crud
from app.schemas.examination import ExaminationCreate, ExaminationRead


router = APIRouter()


@router.post('/')
async def create_examination(
    examination: ExaminationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await examination_crud.create(examination, session)


@router.get('/', response_model=list[ExaminationRead])
async def get_all_notifications(
    session: AsyncSession = Depends(get_async_session)
):
    return await examination_crud.get_multi(session)
