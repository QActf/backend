from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import UnmappedInstanceError


async def delete_obj(
    obj_id: int,
    crud,
    session: AsyncSession,
):
    try:
        db_obj = await crud.get(obj_id, session)
        return await crud.remove(db_obj, session)
    except UnmappedInstanceError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Объект {crud.model.__tablename__} с id {obj_id} не найден.'
        )