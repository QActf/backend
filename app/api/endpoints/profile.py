from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_obj_exists
from app.models import User
from app.schemas.profile import ProfileRead, ProfileCreate
from app.core.db import get_async_session
from app.crud import profile_crud, user_crud
from app.core.user import current_user
from app.services.endpoints_services import delete_obj
from app.core.config import settings
from sqlalchemy import select
from sqlalchemy.orm import selectinload

router = APIRouter()


@router.get('/', response_model=ProfileRead)
async def get_all_profiles(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> ProfileRead:
    """Возвращает все profile юзера."""
    return await profile_crud.get_users_obj(
        user_id=user.id,
        session=session
    )


@router.get('/photo')
async def get_user_photo(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    _user = await session.execute(
        select(User).where(
            User.id == user.id
        ).options(
            selectinload(User.profile)
        )
    )
    _user = _user.scalars().first()
    image: str = _user.profile.image
    return FileResponse(
        f'{settings.base_dir}/{image}'
    )


@router.post('/', response_model=ProfileRead)
async def create_profile(
        profile: ProfileCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Создать Profile"""
    await check_obj_exists(
        obj_id=profile.user_id, crud=user_crud, session=session
    )
    return await profile_crud.create(
        obj_in=profile, user_id=profile.user_id, session=session
    )


@router.delete('/{obj_id}')
async def delete_profile(
        obj_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Удалить объект"""
    return await delete_obj(obj_id=obj_id, crud=profile_crud, session=session)
