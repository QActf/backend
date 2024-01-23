import os
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings


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
