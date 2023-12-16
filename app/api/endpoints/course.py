from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate
from app.schemas.course import CourseCreate, CourseRead
from app.core.db import get_async_session
from app.crud import course_crud
from app.services.endpoints_services import delete_obj

router = APIRouter()


@router.get('/', response_model=list[CourseRead])
async def get_all_courses(
        session: AsyncSession = Depends(get_async_session)
) -> list[CourseRead]:
    """Возвращает все courses."""
    return await course_crud.get_multi(session)


@router.post('/', response_model=CourseRead)
async def create_course(
        course: CourseCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Создать Course"""
    await check_name_duplicate(course.name, CourseCreate, session)
    return await course_crud.create(
        obj_in=course, session=session
    )


@router.delete('/{obj_id}')
async def delete_course(
        obj_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Удалить объект"""
    return await delete_obj(obj_id=obj_id, crud=course_crud, session=session)
