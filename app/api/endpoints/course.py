from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_obj_duplicate, check_obj_exists
from app.api_docs_responses.course import (
    CREATE_COURSE, DELETE_COURSE, GET_COURSE, GET_COURSES, GET_USER_COURSE,
    GET_USER_COURSES, PATCH_COURSE,
)
from app.api_docs_responses.utils_docs import (
    REQUEST_NAME_AND_DESCRIPTION_VALUE,
)
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import course_crud, tariff_crud
from app.models import User
from app.schemas.course import (
    CourseCreate, CourseRead, CourseTariffCreate, CourseUpdate,
    MultiCourseRead,
)
from app.services.endpoints_services import delete_obj
from app.services.utils import (
    Pagination, add_response_headers, get_pagination_params, paginated,
)

router = APIRouter()


@router.get(
    '/',
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
    add_response_headers(response, courses, pagination)
    return paginated(courses, pagination)


@router.get(
    '/me',
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
    add_response_headers(response, courses, pagination)
    return paginated(courses, pagination)


@router.get(
    '/available-started/me',
    response_model=list[MultiCourseRead],
    dependencies=[Depends(current_user)],
    response_model_by_alias=False,
)
async def get_available_started_user_courses(
    response: Response,
    pagination: Pagination = Depends(get_pagination_params),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[MultiCourseRead]:
    """Вернет начатые и доступные по текущей подписке курсы."""
    tariff_courses = list()
    tariff_id = user.tariff_id
    if tariff_id:
        db_tariff = await tariff_crud.get_tariff(
            attr_name='id',
            attr_value=tariff_id,
            session=session,
            courses=True,
        )
        tariff_courses = db_tariff.courses

    user_courses = await course_crud.get_users_obj(
        user_id=user.id,
        session=session,
    )
    all_courses = list(set(tariff_courses + user_courses))
    for course in all_courses:
        setattr(course, 'is_available', course in tariff_courses)
        setattr(course, 'is_started', course in user_courses)

    add_response_headers(response, all_courses, pagination)
    return paginated(all_courses, pagination)


@router.get(
    '/me/{course_id}',
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
    obj = await course_crud.get_course(course_id=course_id, session=session)
    await check_obj_exists(obj=obj)

    if user not in obj.users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Вы не записаны на данный курс.'
        )
    return obj


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
    obj = await course_crud.get_by_attr(
        attr_name='id',
        attr_value=course_id,
        session=session,
    )
    await check_obj_exists(obj=obj)
    return obj


@router.post(
    '/',
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
    """Создаст курс."""
    obj = await course_crud.get_by_attr(
        attr_name='name',
        attr_value=course.name,
        session=session,
    )
    await check_obj_duplicate(obj)
    return await course_crud.create(obj_in=course, session=session)


@router.patch(
    '/{course_id}',
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
    """Обновит курс по его id."""
    obj = await course_crud.get_course(
        course_id=course_id,
        session=session,
    )
    await check_obj_exists(obj=obj)
    return await course_crud.update(
        db_obj=obj,
        obj_in=obj_in,
        session=session,
    )


@router.delete(
    '/{course_id}',
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_204_NO_CONTENT,
    **DELETE_COURSE,
)
async def close_course(
    course_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Удалит курс.
    Нельзя удалить курс, если у него уже есть пользователи,
    можно лишь закрыть доступ новым пользователям.
    """
    obj = await course_crud.get_course(
        course_id=course_id,
        session=session,
    )
    await check_obj_exists(obj=obj)

    if not obj.users:
        await delete_obj(
            obj_id=course_id, crud=course_crud, session=session
        )
        return
    if obj.is_closed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Данный курс уже закрыт.'
        )
    course_closed = await course_crud.close_course(
        course=obj, session=session
    )
    return {
        'course': course_closed,
        'message': 'Курс успешно закрыт.'
    }


@router.post(
    '/course-tariff/',
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED,
)
async def create_course_tariff_association(
    course_tariff: CourseTariffCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создаст связь курса и тарифа."""
    db_course_tariff = await course_crud.get_course_tariff_association(
        course_id=course_tariff.course_id,
        tariff_id=course_tariff.tariff_id,
        session=session,
    )
    await check_obj_duplicate(obj=db_course_tariff)
    db_course = await course_crud.get_by_attr(
        attr_name='id',
        attr_value=course_tariff.course_id,
        session=session,
    )
    await check_obj_exists(obj=db_course)
    db_tariff = await tariff_crud.get_tariff(
        attr_name='id',
        attr_value=course_tariff.tariff_id,
        session=session,
    )
    await check_obj_exists(obj=db_tariff)

    await course_crud.create_course_tariff_association(
        obj_in=course_tariff,
        session=session,
    )


@router.delete(
    '/course-tariff/{course_id}/{tariff_id}',
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_course_tariff_association(
    course_id: int,
    tariff_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалит связь курса и тарифа."""
    await course_crud.delete_course_tariff_association(
        course_id=course_id,
        tariff_id=tariff_id,
        session=session,
    )


@router.post(
    '/start/{course_id}',
    dependencies=[Depends(current_user)],
    status_code=status.HTTP_201_CREATED,
)
async def start_course(
    course_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Создаст связь курса и пользователя. Требуются права пользователя.

    Вернет 400:
    Если у пользователя нет активной подписки.
    Если курса нет в текущем тарифе пользователя.
    """
    if not user.tariff_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нельзя начать курс без активной подписки.'
        )

    db_course = await course_crud.get_by_attr(
        attr_name='id',
        attr_value=course_id,
        session=session,
    )
    await check_obj_exists(obj=db_course)
    db_tariff = await tariff_crud.get_tariff(
        attr_name='id',
        attr_value=user.tariff_id,
        session=session,
        courses=True,
    )
    await check_obj_exists(obj=db_tariff)

    if db_course not in db_tariff.courses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Вы не можете начать курс, так как его нет в вашем тарифе.'
        )

    await course_crud.create_course_user_association(
        course_id=course_id,
        user_id=user.id,
        session=session,
    )
