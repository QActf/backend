from fastapi import APIRouter, Depends
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
    dependencies=[Depends(current_user)]
)
async def get_all_courses(
    session: AsyncSession = Depends(get_async_session),
) -> list[CourseRead]:
    """Возвращает все courses."""
    return await course_crud.get_multi(session)


@router.post(
    "/",
    response_model=CourseRead,
    dependencies=[Depends(current_superuser)]
)
async def create_course(
    course: CourseCreate, session: AsyncSession = Depends(get_async_session)
):
    """Создать Course"""
    await check_name_duplicate(course.name, course_crud, session)
    return await course_crud.create(obj_in=course, session=session)


@router.delete("/{obj_id}", dependencies=[Depends(current_superuser)])
async def delete_course(
    obj_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить объект"""
    return await delete_obj(obj_id=obj_id, crud=course_crud, session=session)


@router.get(
    "/{obj_id}",
    response_model=CourseRead,
    dependencies=[Depends(current_user)]
)
async def get_id_course(
    obj_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> CourseRead:
    """Возвращает Course по его id."""
    await check_obj_exists(obj_id=obj_id, crud=course_crud, session=session)
    return await course_crud.get(obj_id=obj_id, session=session)


@router.patch(
    "/{obj_id}",
    response_model=CourseRead,
    dependencies=[Depends(current_superuser)]
)
async def update_course(
    obj_id: int,
    obj_in: CourseUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CourseRead:
    """Обновляет Course по его id."""
    course = await course_crud.get(obj_id=obj_id, session=session)
    await check_obj_exists(
        obj_id=obj_id, crud=course_crud, session=session
    )
    if obj_in.name is not None:
        await check_name_duplicate(
            name=obj_in.name, crud=course_crud, session=session
        )
    return await course_crud.update(
        db_obj=course, obj_in=obj_in, session=session
    )
