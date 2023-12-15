from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate
from app.schemas.course import CourseCreate, CourseRead
from app.core.db import get_async_session
from app.crud import course_crud

router = APIRouter()


@router.get('/', response_model=List[CourseRead])
async def get_all_courses(
        session: AsyncSession = Depends(get_async_session)
) -> List[CourseRead]:
    """Возвращает все courses."""
    return await course_crud.get_multi(session)


@router.post('/', response_model=CourseRead)
async def create_course(
        course: CourseCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Создать Course"""
    await check_name_duplicate(course.name, CourseCreate, session)
    course = await course_crud.create(
        obj_in=course, session=session
    )
    return course


@router.delete('/')
async def delete_course(
        obj_id: str,
        session: AsyncSession = Depends(get_async_session),
):
    """Удалить объект"""
    course = await course_crud.get(obj_id=obj_id, session=session)
    return await course_crud.remove(db_obj=course, session=session)
