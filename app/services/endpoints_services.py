from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.crud import tariff_crud
from app.schemas.tariff import TariffPlanRead


async def delete_obj(
    obj_id: int,
    crud,
    session: AsyncSession,
):
    try:
        db_obj = await crud.get_by_attr(
            attr_name='id',
            attr_value=obj_id,
            session=session,
        )
        return await crud.remove(db_obj, session)
    except UnmappedInstanceError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Объект {crud.model.__tablename__}'
                   f' с id {obj_id} не найден.'
        )


def get_courses_with_tariff_flags(db_courses, db_tariffs, user):
    courses_with_tariff_flags = list()
    for course in db_courses:
        if not (course.is_closed and user not in course.users):
            tariff_flags = dict()
            true_tariffs_count = 0
            for tariff in db_tariffs:
                if not (tariff.is_closed and user not in tariff.users):
                    tariff_flags[tariff.name] = course in tariff.courses
                    if course in tariff.courses:
                        true_tariffs_count += 1
            courses_with_tariff_flags.append(
                {
                    'name': course.name,
                    'true_tariffs_count': true_tariffs_count,
                    **tariff_flags
                }
            )
    return courses_with_tariff_flags


async def get_tariffs_with_extra(db_tariffs, user, session):
    user_tariff_cost = None
    if user.tariff_id:
        db_user_tariff = await tariff_crud.get_tariff(
            attr_name='id',
            attr_value=user.tariff_id,
            session=session,
        )
        if db_user_tariff:
            user_tariff_cost = db_user_tariff.cost

    tariffs = [TariffPlanRead(id=0, name='', description='', cost=0,
                              dataIndex='name', key='name', is_active=False,
                              this_tariff=False)]
    for tariff in db_tariffs:
        if not (tariff.is_closed and user not in tariff.users):
            tariff.dataIndex = tariff.name
            tariff.key = tariff.name
            tariff.this_tariff = tariff.id == user.tariff_id
            tariff.is_active = (
                False if user_tariff_cost is None
                else tariff.cost <= user_tariff_cost
            )
            tariffs.append(tariff)
    return tariffs
