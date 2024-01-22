from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate, check_obj_exists
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import examination_crud
from app.schemas.examination import ExaminationCreate, ExaminationRead, ExaminationUpdate
from app.services.endpoints_services import delete_obj

router = APIRouter()


@router.get(
    "/",
    response_model=list[ExaminationRead],
    dependencies=[Depends(current_user)]
)
async def get_all_examinations(
    session: AsyncSession = Depends(get_async_session),
) -> list[ExaminationRead]:
    """Возвращает все Examination."""
    return await examination_crud.get_multi(session)


@router.get(
    "/{examination_id}",
    response_model=ExaminationRead,
    dependencies=[Depends(current_user)]
)
async def get_examination(
        examination_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> ExaminationRead:
    """Возвращает examination."""
    await check_obj_exists(examination_id, examination_crud, session)
    return await examination_crud.get(examination_id, session=session)


@router.post(
    "/",
    response_model=ExaminationRead,
    dependencies=[Depends(current_superuser)]
)
async def create_examination(
    examination: ExaminationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создать Examination"""
    await check_name_duplicate(examination.name, examination_crud, session)
    return await examination_crud.create(
        obj_in=examination, session=session
    )


@router.patch(
    "/{examination_id}",
    response_model=ExaminationRead,
    dependencies=[Depends(current_user)]
)
async def update_examination(
        examination_id: int,
        examination: ExaminationUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """Обновляет Examination"""
    await check_obj_exists(examination.id, examination_crud, session)
    _examination = await examination_crud.get(examination_id, session=session)
    return await examination_crud.update(_examination, examination, session)


@router.delete(
    "/{obj_id}",
    dependencies=[Depends(current_superuser)]
)
async def delete_examination(
    obj_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить объект"""
    return await delete_obj(
        obj_id=obj_id, crud=examination_crud, session=session
    )
