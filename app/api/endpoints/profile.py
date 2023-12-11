from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import profile_crud
from app.schemas.profile import ProfileCreate, ProfileRead


router = APIRouter()


@router.post('/{user_id}', response_model=ProfileRead)
async def create_profile(
    user_id: int,
    profile: ProfileCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await profile_crud.create(profile, user_id, session)


@router.get('/', response_model=list[ProfileRead])
async def get_all_profiles(
    session: AsyncSession = Depends(get_async_session)
):
    return await profile_crud.get_multi(session)
