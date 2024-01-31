from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate, check_obj_exists
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import course_crud, user_crud
from app.models import Course, User
from app.schemas.course import CourseCreate, CourseRead, CourseUpdate
from app.services.endpoints_services import delete_obj
from app.services.utils import (Pagination, add_response_headers,
                                get_pagination_params, paginated)

router = APIRouter()


@router.get(
    "/",
    response_model=list[CourseRead],
    dependencies=[Depends(current_superuser)]
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
    dependencies=[Depends(current_user)]
)
async def get_all_user_courses(
    response: Response,
    pagination: Pagination = Depends(get_pagination_params),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[CourseRead]:
    """Возвращает все курсы пользователя, выполняющего запрос."""
    courses = await course_crud.get_user_courses(
        user_id=user.id, session=session
    )
    response = add_response_headers(response, courses, pagination)
    return paginated(courses, pagination)


@router.get(
    "/me/{course_id}",
    response_model=CourseRead,
    dependencies=[Depends(current_user)]
)
async def get_user_course_id(
    course_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> CourseRead:
    """Возвращает конкретный курс пользователя, выполняющего запрос."""
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
    "/{course_id}",
    response_model=CourseRead,
    dependencies=[Depends(current_user)]
)
async def get_id_course(
    course_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> CourseRead:
    """Возвращает курс по его id."""
    await check_obj_exists(obj_id=course_id, crud=course_crud, session=session)
    return await course_crud.get(obj_id=course_id, session=session)


@router.put(
    "/",
    response_model=CourseRead,
    dependencies=[Depends(current_superuser)]
)
async def update_users_course(
    course_id: int,
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> CourseRead:
    """Привязывает курс к пользователю."""
    await check_obj_exists(course_id, course_crud, session)
    await check_obj_exists(user_id, user_crud, session)
    course = await course_crud.get_course(
        course_id=course_id, session=session
    )
    user = await user_crud.get(
        obj_id=user_id, session=session
    )
    if user in course.users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='На данный курс уже записан указанный пользователь.'
        )
    if course.is_closed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Данный курс закрыт, нельзя добавлять к нему пользователей.'
        )
    return await course_crud.add_user(
        course=course, user=user, session=session
    )


@router.post(
    "/",
    response_model=CourseRead,
    dependencies=[Depends(current_superuser)]
)
async def create_course(
    course: CourseCreate, session: AsyncSession = Depends(get_async_session)
):
    """Создать курс."""
    await check_name_duplicate(course.name, course_crud, session)
    return await course_crud.create(obj_in=course, session=session)


@router.patch(
    "/{course_id}",
    response_model=CourseRead,
    dependencies=[Depends(current_superuser)]
)
async def update_course(
    course_id: int,
    obj_in: CourseUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CourseRead:
    """Обновляет курс по его id."""
    course = await course_crud.get(obj_id=course_id, session=session)
    await check_obj_exists(
        obj_id=course_id, crud=course_crud, session=session
    )
    if obj_in.name is not None:
        await check_name_duplicate(
            name=obj_in.name, crud=course_crud, session=session
        )
    return await course_crud.update(
        db_obj=course, obj_in=obj_in, session=session
    )


@router.delete("/{course_id}", dependencies=[Depends(current_superuser)])
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
        course_delete = await delete_obj(
            obj_id=course_id, crud=course_crud, session=session
        )
        return {
            'course': course_delete,
            'message': 'Курс успешно удалён'
        }
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
