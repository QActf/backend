from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import course_crud
from app.schemas.course import CourseCreate, CourseRead


router = APIRouter()


@router.post('/')
async def create_course(
    course: CourseCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await course_crud.create(course, session)


@router.get('/', response_model=list[CourseRead])
async def get_all_courses(
    session: AsyncSession = Depends(get_async_session)
):
    return await course_crud.get_multi(session)
