import re

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud import profile_crud
from app.models import Profile, User
from app.schemas.profile import ProfileRead, ProfileUpdate
from app.services.utils import create_filename, remove_content, save_content

router = APIRouter()


@router.get(
    '/',
    response_model=ProfileRead,
    dependencies=[Depends(current_user)]
)
async def get_current_user_profile(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> ProfileRead:
    """Возвращает profile юзера."""
    return await profile_crud.get_users_obj(
        user_id=user.id,
        session=session
    )


@router.get(
    '/photo',
    dependencies=[Depends(current_user)]
)
async def get_user_photo(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Возвращает фото профиля."""
    return await profile_crud.get_user_photo(user.id, session)


@router.patch(
    '/',
    response_model=ProfileRead,
    dependencies=[Depends(current_user)]
)
async def update_profile(
        profile: ProfileUpdate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    _profile = await profile_crud.get_users_obj(user.id, session)
    return await profile_crud.update(_profile, profile, session)


@router.patch(
    '/update_photo',
    response_model=ProfileRead,
    dependencies=[Depends(current_user)]
)
async def update_photo(
        file: UploadFile = File(...),
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Обновить фото профиля."""
    _profile: Profile = await profile_crud.get_users_obj(user.id, session)
    if not re.match(r'^.+cat\d+\.png$', _profile.image):
        remove_content(_profile.image)
    file.filename: str = create_filename(file)
    await save_content(file)
    return await profile_crud.update_photo(
        user.id,
        file.filename,
        session
    )


@router.post('/', response_model=ProfileRead, deprecated=True)
def create_profile():
    """Профиль создаётся при создании юзера."""
    raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail=('Профиль создаётся автоматически при создании пользователя. '
                'Используйте метод PATCH.')
    )


@router.delete('/{obj_id}', deprecated=True)
def delete_profile(obg_id: str):
    """Удалить объект"""
    raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail='Профиль удаляется при удалении пользователя.'
    )
