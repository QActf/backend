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
from app.services.endpoints_services import (
    get_courses_with_tariff_flags, get_tariffs_with_extra,
)

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
    Если тариф закрыт и нет связи тариф-пользователь, то он будет исключен из
    ответа.
    Сортировка курсов происходит по количеству тарифов с флагом True.
    Сортировка тарифных планов происходит по полю cost.
    """
    db_courses = await course_crud.get_multi_courses_with_users(
        session=session,
    )
    db_tariffs = await tariff_crud.get_tariff(
        courses=True,
        users=True,
        multi=True,
        session=session,
        order_by_cost=True,
    )

    courses_with_tariff_flags = get_courses_with_tariff_flags(
        db_courses=db_courses,
        db_tariffs=db_tariffs,
        user=user,
    )
    sorted_courses_with_tariff_flags = sorted(
        courses_with_tariff_flags,
        key=lambda cour: cour['true_tariffs_count'],
        reverse=True,
    )
    for course in sorted_courses_with_tariff_flags:
        course.pop('true_tariffs_count', None)

    tariffs_with_extra = await get_tariffs_with_extra(
        db_tariffs=db_tariffs,
        user=user,
        session=session,
    )

    response = PlanRead(
        courses=sorted_courses_with_tariff_flags,
        tariffs=tariffs_with_extra,
    )
    return response
