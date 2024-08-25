from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.validators import check_obj_duplicate, check_obj_exists
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import notification_crud, user_crud
from app.models import User
from app.schemas.notification import (
    AddNotificationForUser, NotificationCreate, NotificationRead,
    ReadNotificationForUser,
)
from app.services.utils import (
    Pagination, add_response_headers, get_pagination_params, paginated,
)

router = APIRouter()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(current_superuser)],
)
async def create_notification(
    notification: NotificationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создаст уведомление."""
    obj = await notification_crud.get_by_attr(
        attr_name='name',
        attr_value=notification.name,
        session=session,
    )
    await check_obj_duplicate(obj=obj)
    await notification_crud.create(obj_in=notification, session=session)


@router.get(
    '/',
    response_model=list[NotificationRead],
    dependencies=[Depends(current_superuser)],
)
async def get_all_notifications(
    session: AsyncSession = Depends(get_async_session),
):
    """Вернет список всех уведомлений."""
    return await notification_crud.get_multi(session=session)


@router.delete(
    '/{notification_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(current_superuser)],
)
async def delete_notification(
    notification_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Удалит уведомление."""
    obj = await notification_crud.get_by_attr(
        attr_name='id',
        attr_value=notification_id,
        session=session,
    )
    await check_obj_exists(obj=obj)
    await notification_crud.remove(
        db_obj=obj,
        session=session,
    )


@router.post(
    '/add-for-user',
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(current_superuser)],
)
async def add_notification_for_user(
    notification: AddNotificationForUser,
    session: AsyncSession = Depends(get_async_session)
):
    """Создаст связь пользователя и уведомления."""
    db_user = await user_crud.get_by_attr(
        attr_name='id',
        attr_value=notification.user_id,
        session=session,
    )
    await check_obj_exists(db_user)
    db_notification = await notification_crud.get_by_attr(
        attr_name='id',
        attr_value=notification.notification_id,
        session=session,
    )
    await check_obj_exists(db_notification)

    await notification_crud.add_notification_for_user(
        obj_in=notification,
        session=session,
    )


@router.get(
    '/get-for-user',
    response_model=list[ReadNotificationForUser],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
)
async def get_notifications_for_user(
    response: Response,
    pagination: Pagination = Depends(get_pagination_params),
    user: User = Depends(current_user),
    viewed: bool = Query(default=False, alias='viewed'),
    bell: bool = Query(default=False, alias='bell'),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Вернет список уведомлений для пользователя.

    Параметры:
    - **viewed**: (bool) Если True, вернет прочитанные уведомления.
    По умолчанию False.
    - **bell**: (bool) Если True, вернет непрочитанные уведомления без поля
    message. Дополнительно указывать параметр viewed не требуется.
    По умолчанию False.
    """
    notifications = await notification_crud.get_user_notifications(
        user_id=user.id,
        viewed=viewed,
        bell=bell,
        session=session,
    )
    add_response_headers(response, notifications, pagination)
    return paginated(notifications, pagination)


@router.patch(
    '/mark-as-viewed/{user_notification_id}',
    dependencies=[Depends(current_user)],
)
async def mark_as_viewed(
    user_notification_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Пометит уведомление как прочитанное."""
    obj = await notification_crud.get_user_notification_by_id(
        obj_id=user_notification_id,
        user_id=user.id,
        session=session,
    )
    await check_obj_exists(obj=obj)
    await notification_crud.mark_user_notification_as_viewed(
        obj_id=user_notification_id,
        session=session,
    )
