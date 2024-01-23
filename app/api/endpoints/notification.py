from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import notification_crud
from app.schemas.notification import NotificationCreate, NotificationRead

router = APIRouter()


@router.post("/", dependencies=[Depends(current_superuser)])
async def create_notification(
    notification: NotificationCreate,
        session: AsyncSession = Depends(get_async_session)
):
    return await notification_crud.create(notification, session)


@router.get(
    "/",
    response_model=list[NotificationRead],
    dependencies=[Depends(current_user)]
)
async def get_all_notifications(
        session: AsyncSession = Depends(get_async_session)
):
    return await notification_crud.get_multi(session)
