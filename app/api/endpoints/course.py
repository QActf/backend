from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate, check_obj_exists
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import course_crud
from app.schemas.course import CourseCreate, CourseRead, CourseUpdate
from app.services.endpoints_services import delete_obj

router = APIRouter()


@router.get(
    "/",
    response_model=list[CourseRead],
)
async def get_all_courses(
    session: AsyncSession = Depends(get_async_session),
) -> list[CourseRead]:
    """Возвращает все courses."""
    return await course_crud.get_multi(session)


@router.get(
        '/{course_id}',
        response_model=CourseRead,
)
async def get_course(
    course_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает курс."""
    await check_obj_exists(course_id, course_crud, session)
    return await course_crud.get(course_id, session)


@router.post(
    "/",
    response_model=CourseRead,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED
)
async def create_course(
    course: CourseCreate, session: AsyncSession = Depends(get_async_session)
):
    """Создать Course"""
    await check_name_duplicate(course.name, course_crud, session)
    return await course_crud.create(obj_in=course, session=session)


@router.patch(
        '/{course_id}',
        response_model=CourseRead,
        dependencies=[Depends(current_superuser)]
)
async def update_course(
    course_id: int,
    data: CourseUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Апдейт курса."""
    if data.name:
        await check_name_duplicate(data.name, course_crud, session)
    _course = await check_obj_exists(course_id, course_crud, session)
    return await course_crud.update(_course, data, session)


@router.delete("/{obj_id}", dependencies=[Depends(current_superuser)],
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    obj_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить объект"""
    return await delete_obj(obj_id=obj_id, crud=course_crud, session=session)
