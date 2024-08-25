from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.validators import check_obj_exists
from app.core.db import get_async_session
from app.core.user import (
    UserManager, current_superuser, current_user, get_user_manager,
)
from app.crud import course_crud, tariff_crud, user_crud
from app.models import User
from app.schemas.subscription import PlanRead, SubscriptionCreate
from app.schemas.user import UserTariffDelete, UserTariffUpdate

router = APIRouter()


@router.post(
    '/',
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_200_OK,
)
async def add_subscription(
    subscription: SubscriptionCreate,
    user_manager: UserManager = Depends(get_user_manager),
    session: AsyncSession = Depends(get_async_session),
):
    """Оформит подписку (задаст тариф в объекте пользователя)."""
    db_tariff = await tariff_crud.get_tariff(
        attr_name='id',
        attr_value=subscription.tariff_id,
        session=session,
    )
    await check_obj_exists(obj=db_tariff)
    if db_tariff.is_closed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нельзя оформить подписку. Тариф закрыт.'
        )
    db_user = await user_crud.get_by_attr(
        attr_name='id',
        attr_value=subscription.user_id,
        session=session,
    )
    await check_obj_exists(obj=db_user)

    user_update = UserTariffUpdate(tariff_id=subscription.tariff_id)
    await user_manager.update(
        user_update=user_update,
        user=db_user,
        safe=True,
    )


@router.delete(
    '/{user_id}',
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_subscription(
    user_id: int,
    user_manager: UserManager = Depends(get_user_manager),
    session: AsyncSession = Depends(get_async_session),
):
    """Отзовет подписку у пользователя."""
    db_user = await user_crud.get_by_attr(
        attr_name='id',
        attr_value=user_id,
        session=session,
    )
    await check_obj_exists(obj=db_user)

    user_update = UserTariffDelete(tariff_id=None)
    await user_manager.update(
        user_update=user_update,
        user=db_user,
        safe=True,
    )


@router.get(
    '/plans',
    response_model=PlanRead,
    dependencies=[Depends(current_user)],
)
async def get_tariff_planes(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> PlanRead:
    """
    Получение тарифных планов.

    Если курс закрыт и нет связи курс-пользователь, то он будет исключен из
    ответа.
    """
    courses = await course_crud.get_multi_courses_with_users(session=session)
    tariffs = await tariff_crud.get_tariff(
        courses=True,
        multi=True,
        is_closed=False,
        session=session,
    )

    courses_with_tariff_flags = list()
    for course in courses:
        if course.is_closed and user not in course.users:
            continue
        tariff_flags = dict()
        for tariff in tariffs:
            tariff_flags[tariff.name] = course in tariff.courses
        courses_with_tariff_flags.append(
            {
                'name': course.name,
                **tariff_flags
            }
        )

    for tariff in tariffs:
        setattr(tariff, 'dataIndex', tariff.name)
        setattr(tariff, 'key', tariff.name)

    response = PlanRead(
        courses=courses_with_tariff_flags,
        tariffs=tariffs,
    )
    return response
