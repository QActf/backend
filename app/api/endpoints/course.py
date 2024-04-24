from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate, check_obj_exists
from app.api_docs_responses.course import (CREATE_COURSE, DELETE_COURSE,
                                           GET_COURSE, GET_COURSES,
                                           GET_USER_COURSE, GET_USER_COURSES,
                                           PATCH_COURSE)
from app.api_docs_responses.utils_docs import \
    REQUEST_NAME_AND_DESCRIPTION_VALUE
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import course_crud
from app.models import Course, User
from app.schemas.course import CourseCreate, CourseRead, CourseUpdate
from app.services.endpoints_services import delete_obj
from app.services.utils import (Pagination, add_response_headers,
                                get_pagination_params, paginated)

router = APIRouter()


@router.get(
    "/",
    response_model=list[CourseRead],
    **GET_COURSES,
)
async def get_all_courses(
    response: Response,
    pagination: Pagination = Depends(get_pagination_params),
    session: AsyncSession = Depends(get_async_session),
) -> list[CourseRead]:
    """Возвращает все курсы."""
    courses = await course_crud.get_multi(session)
    response = add_response_headers(response, courses, pagination)
    return paginated(courses, pagination)


@router.get(
    "/me",
    response_model=list[CourseRead],
    dependencies=[Depends(current_user)],
    **GET_USER_COURSES,
)
async def get_all_user_courses(
    response: Response,
    pagination: Pagination = Depends(get_pagination_params),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[CourseRead]:
    """Возвращает все курсы текущего пользователя."""
    courses = await course_crud.get_users_obj(
        user_id=user.id, session=session
    )
    response = add_response_headers(response, courses, pagination)
    return paginated(courses, pagination)


@router.get(
    "/me/{course_id}",
    response_model=CourseRead,
    dependencies=[Depends(current_user)],
    **GET_USER_COURSE,
)
async def get_user_course_id(
    course_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> CourseRead:
    """Возвращает конкретный курс текущего пользователя по id."""
    await check_obj_exists(
        obj_id=course_id, crud=course_crud, session=session
    )
    course: Course | None = await course_crud.get_course(
        course_id=course_id,
        session=session
    )
    if user not in course.users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Вы не записаны на данный курс.'
        )
    return course


@router.get(
    '/{course_id}',
    response_model=CourseRead,
    **GET_COURSE,
)
async def get_course(
    course_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает курс по id."""
    await check_obj_exists(course_id, course_crud, session)
    return await course_crud.get(course_id, session)


@router.post(
    "/",
    response_model=CourseRead,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED,
    **CREATE_COURSE,
)
async def create_course(
    course: CourseCreate = Body(
        openapi_examples=REQUEST_NAME_AND_DESCRIPTION_VALUE),
    session: AsyncSession = Depends(get_async_session)
):
    """Создать курс."""
    await check_name_duplicate(course.name, course_crud, session)
    return await course_crud.create(obj_in=course, session=session)


@router.patch(
    "/{course_id}",
    response_model=CourseRead,
    dependencies=[Depends(current_superuser)],
    **PATCH_COURSE,
)
async def update_course(
    course_id: int,
    obj_in: CourseUpdate = Body(
        openapi_examples=REQUEST_NAME_AND_DESCRIPTION_VALUE),
    session: AsyncSession = Depends(get_async_session),
) -> CourseRead:
    """Обновляет курс по его id."""
    course = await check_obj_exists(
        obj_id=course_id, crud=course_crud, session=session
    )
    if obj_in.name:
        await check_name_duplicate(
            name=obj_in.name, crud=course_crud, session=session
        )
    return await course_crud.update(
        db_obj=course, obj_in=obj_in, session=session
    )


@router.delete(
    "/{course_id}",
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_204_NO_CONTENT,
    **DELETE_COURSE,
)
async def close_course(
    course_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Удаляет курс.
    Нельзя удалить курс, если у него уже есть пользователи,
    можно лишь закрыть доступ новым пользователям.
    """
    await check_obj_exists(
        obj_id=course_id, crud=course_crud, session=session
    )
    course = await course_crud.get_course(
        course_id=course_id, session=session
    )
    if not course.users:
        await delete_obj(
            obj_id=course_id, crud=course_crud, session=session
        )
        return
    if course.is_closed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Данный курс уже закрыт.'
        )
    course_closed = await course_crud.close_course(
        course=course, session=session
    )
    return {
        'course': course_closed,
        'message': 'Курс успешно закрыт'
    }
