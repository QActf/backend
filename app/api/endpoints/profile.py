import re

from fastapi import (
    APIRouter, Body, Depends, File, HTTPException, Response, UploadFile, status
)
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.filters import ProfileFilter
from app.api_docs_responses.profile import (
    CREATE_PROFILE, DELETE_PROFILE, GET_ME_PROFILE, GET_PROFILE,
    GET_PROFILE_PHOTO, GET_PROFILES, UPDATE_PROFILE, UPDATE_PROFILE_PHOTO
)
from app.api_docs_responses.utils_docs import PROFILE_UPDATE_VALUE
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import profile_crud
from app.models import Profile, User
from app.schemas.profile import ProfileRead, ProfileUpdate
from app.services.utils import (
    Pagination, add_response_headers, create_filename, get_pagination_params,
    paginated, remove_content, save_content
)

router = APIRouter()


@router.get(
    '/',
    response_model=list[ProfileRead],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    **GET_PROFILES,
)
async def get_all_profiles(
    response: Response,
    profile_filter: ProfileFilter = FilterDepends(ProfileFilter),
    session: AsyncSession = Depends(get_async_session),
    pagination: Pagination = Depends(get_pagination_params)
):
    """Возвращает все профили."""
    profiles = await profile_crud.get_profile_filter(
        profile_filter, session
    )
    response = add_response_headers(
        response, profiles, pagination
    )
    return paginated(profiles, pagination)


@router.get(
    '/me',
    response_model=ProfileRead,
    response_model_exclude_none=True,
    **GET_ME_PROFILE,
)
async def get_current_user_profile(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> ProfileRead:
    """Возвращает профиль текущего пользователя."""
    return await profile_crud.get_users_obj(
        user_id=user.id,
        session=session
    )


@router.get(
    '/{profile_id}',
    response_model=ProfileRead,
    dependencies=[Depends(current_superuser)],
    **GET_PROFILE
)
async def get_profile(
    profile_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> ProfileRead:
    """Возвращает профиль пользователя по id."""
    return await profile_crud.get(profile_id, session)


@router.get(
    '/me/photo',
    dependencies=[Depends(current_user)],
    **GET_PROFILE_PHOTO
)
async def get_user_photo(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает фото профиля."""
    return await profile_crud.get_user_photo(user.id, session)


@router.patch(
    '/me',
    response_model=ProfileRead,
    dependencies=[Depends(current_user)],
    **UPDATE_PROFILE,
)
async def update_profile(
    profile: ProfileUpdate = Body(example=PROFILE_UPDATE_VALUE),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Обновить профиль текущего пользователя."""
    _profile = await profile_crud.get_users_obj(user.id, session)
    return await profile_crud.update(_profile, profile, session)


@router.patch(
    '/me/update_photo',
    response_model=ProfileRead,
    dependencies=[Depends(current_user)],
    **UPDATE_PROFILE_PHOTO
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
    file.filename = create_filename(file)
    await save_content(file)
    return await profile_crud.update_photo(
        user.id,
        file.filename,
        session
    )


@router.post(
    '/me',
    response_model=ProfileRead,
    deprecated=True,
    **CREATE_PROFILE,
)
def create_profile():
    """Профиль создаётся при создании юзера."""
    raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail=('Профиль создаётся автоматически при создании пользователя. '
                'Используйте метод PATCH.')
    )


@router.delete(
    '/{profile_id}',
    deprecated=True,
    status_code=status.HTTP_204_NO_CONTENT,
    **DELETE_PROFILE,
)
def delete_profile():
    """Профиль удаляется при удалении пользователя."""
    raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail='Профиль удаляется при удалении пользователя.'
    )
