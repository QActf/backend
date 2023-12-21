from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate
from app.core.db import get_async_session
from app.crud import examination_crud
from app.schemas.examination import ExaminationCreate, ExaminationRead
from app.services.endpoints_services import delete_obj

router = APIRouter()


@router.get("/", response_model=list[ExaminationRead])
async def get_all_examinations(
    session: AsyncSession = Depends(get_async_session),
) -> list[ExaminationRead]:
    """Возвращает все Examination."""
    return await examination_crud.get_multi(session)


@router.post("/", response_model=ExaminationRead)
async def create_examination(
    examination: ExaminationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создать Examination"""
    await check_name_duplicate(examination.name, examination_crud, session)
    return await examination_crud.create(
        obj_in=examination, session=session
    )


@router.delete("/{obj_id}")
async def delete_examination(
    obj_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить объект"""
    return await delete_obj(
        obj_id=obj_id, crud=examination_crud, session=session
    )
