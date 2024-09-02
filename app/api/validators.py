from http import HTTPStatus

from fastapi import HTTPException


async def check_obj_exists(obj):
    if not obj:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Объект не найден.',
        )


async def check_obj_duplicate(obj):
    if obj:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Объект с таким именем уже существует.',
        )


async def check_difficult_task(data):
    if data.difficult not in range(1, 10):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Сложность задачи должна быть в диапазоне [1, 9].',
        )
