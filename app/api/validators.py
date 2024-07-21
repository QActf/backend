from http import HTTPStatus

from fastapi import HTTPException


async def check_obj_exists(obj):
    if not obj:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Объект не найден.',
        )


async def check_obj_duplicate(obj):
    if obj:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Объект с таким именем уже существует.',
        )
