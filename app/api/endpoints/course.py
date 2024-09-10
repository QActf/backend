import re

from fastapi import (
    APIRouter, Body, Depends, File, HTTPException, Response, UploadFile,
    status,
)
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_obj_duplicate, check_obj_exists
from app.api_docs_responses.course import (
    CREATE_COURSE, DELETE_COURSE, GET_COURSE, GET_COURSES, GET_USER_COURSE,
    GET_USER_COURSES, PATCH_COURSE, PATCH_COURSE_ICON,
)
from app.api_docs_responses.utils_docs import (
    COURSE_VALUE, REQUEST_NAME_AND_DESCRIPTION_VALUE,
)
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import course_crud, tariff_crud
from app.models import Course, User
from app.models.task import tasks_solved_user_association
from app.schemas.course import (
    CourseCreate, CourseRead, CourseTariffCreate, CourseTasksRead,
    CourseUpdate, MultiCourseForUserRead,
)
from app.services.endpoints_services import delete_obj
from app.services.utils import (
    Pagination, add_response_headers, create_filename, get_pagination_params,
    paginated, remove_content, save_content,
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
    response_model=list[MultiCourseForUserRead],
    dependencies=[Depends(current_user)],
)
async def get_available_started_user_courses(
    response: Response,
    pagination: Pagination = Depends(get_pagination_params),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[MultiCourseForUserRead]:
    """Вернет начатые и доступные по текущей подписке курсы."""
    tariff_id = user.tariff_id
    tariff_courses = set()
    if tariff_id:
        db_tariff = await tariff_crud.get_tariff(
            attr_name='id',
            attr_value=tariff_id,
            session=session,
            courses=True,
        )
        tariff_courses = set(db_tariff.courses) if db_tariff.courses else set()

    user_courses = set(await course_crud.get_users_obj(
        user_id=user.id,
        session=session,
    ))

    all_courses = tariff_courses.union(user_courses)
    common_courses = tariff_courses.intersection(user_courses)

    for course in all_courses:
        if course.in_development:
            course.status = 'in_development'
        elif course in common_courses:
            course.status = 'started'
        elif course in tariff_courses and not course.is_closed:
            course.status = 'available'
        else:
            course.status = 'unavailable'

    all_courses = list(all_courses)
    add_response_headers(response, all_courses, pagination)
    return paginated(all_courses, pagination)


@router.get(
    '/me/{course_id}',
    response_model=CourseTasksRead,
    dependencies=[Depends(current_user)],
    **GET_USER_COURSE,
)
async def get_user_course_id(
    course_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> CourseTasksRead:
    """Возвращает конкретный курс текущего пользователя по id."""
    obj = await course_crud.get_course(course_id=course_id, session=session)
    await check_obj_exists(obj=obj)

    if user not in obj.users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Вы не записаны на данный курс.'
        )
    for task in obj.tasks:
        stmt = select(tasks_solved_user_association).where(
            and_(
                tasks_solved_user_association.c.task_id == task.id,
                tasks_solved_user_association.c.user_id == user.id
            )
        )
        obj_task = await session.execute(stmt)
        task.done = bool(obj_task.scalars().first())
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
        openapi_examples=COURSE_VALUE),
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


@router.patch(
    '/update_icon/{course_id}',
    response_model=CourseRead,
    dependencies=[Depends(current_superuser)],
    **PATCH_COURSE_ICON,
)
async def update_photo(
    course_id: int,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session)
):
    """Обновить icon курса."""
    course: Course = await course_crud.get_course(
        course_id=course_id, session=session
    )
    await check_obj_exists(obj=course)
    if not re.match(r'^.+icon\d+\.png$', course.icon):
        remove_content(course.icon)
    file.filename = create_filename(file, 'icon_course')
    await save_content(file)
    return await course_crud.update_icon(
        course.id,
        file.filename,
        session
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
    if db_course.is_closed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нельзя начать закрытый курс.'
        )
    if db_course.in_development:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нельзя начать курс, который ещё в разработке.'
        )

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
