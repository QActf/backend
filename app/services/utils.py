import os
from collections import namedtuple
from typing import Any, Sequence
from uuid import uuid4

from fastapi import Query, Response, UploadFile

from app.core.config import settings


class Pagination(namedtuple('Pagination', 'offset limit')):
    __slots__ = ()

    @property
    def end(self):
        return self.offset + self.limit


def create_filename(file: UploadFile) -> str:
    """Создаёт имя файла."""
    file_extension = file.filename.split('.')[-1]
    return f'{uuid4()}.{file_extension}'


async def save_content(file: UploadFile):
    """Сохранение файла в файловой системе."""
    contents = await file.read()
    with open(f'{settings.media_url}{file.filename}', 'wb') as f:
        f.write(contents)


def remove_content(path: str) -> None:
    """Удаление файла."""
    os.remove(f'{settings.base_dir}/{settings.media_url}{path}')


def get_pagination_params(
    # offset must be greater than or equal to 0
    offset: int = Query(settings.offset, ge=0),
    # limit must be greater than 0
    limit: int = Query(settings.limit, gt=0)
):
    return Pagination(offset, limit)


def paginated(
        data: Sequence[Any], paginator: Pagination
) -> Sequence[Any]:
    """Возвращает срез переданной последовательности."""
    return data[paginator.offset:paginator.end]


def add_response_headers(
        response: Response,
        sequence: Sequence[Any],
        paginator: Pagination
) -> Response:
    response.headers['X-Total-Count'] = str(len(sequence))
    response.headers['X-Offset'] = str(paginator.offset)
    response.headers['X-Limit'] = str(paginator.limit)
    return response
