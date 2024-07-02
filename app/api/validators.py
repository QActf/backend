from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def check_obj_exists(
    obj_id: int,
    crud,
    session: AsyncSession,
):
    obj = await crud.get(obj_id, session)
    if obj is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Объект {crud.model.__tablename__} '
                   f'с id {obj_id} не найден.',
        )
    return obj


async def check_name_duplicate(
    name: str,
    crud,
    session: AsyncSession,
) -> None:
    obj = await crud.get_obj_by_name(name, session)
    if obj is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Объект {crud.model.__tablename__}'
            f' с таким именем уже существует!',
        )
