from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.filters import ProfileFilter
from app.core.config import settings
from app.crud.base import CRUDBase
from app.models import Profile, User
from app.schemas.profile import ProfileCreate


class CRUDProfile(CRUDBase):

    async def get_profile_filter(
            self,
            profile_filter: ProfileFilter,
            sesion: AsyncSession
    ):
        query_filter = profile_filter.filter(select(self.model))
        db_objs = await sesion.execute(
            query_filter
            .options(
                selectinload(self.model.achievements)
            )
        )
        return db_objs.scalars().all()

    async def get_multi(self, session: AsyncSession):
        db_objs = await session.execute(
            select(self.model)
            .options(
                selectinload(Profile.achievements)
            )
        )
        return db_objs.scalars().all()

    async def get(self, obj_id: int, session: AsyncSession):
        profile = await session.execute(
            select(self.model)
            .options(
                selectinload(Profile.achievements)
            )
        )
        return profile.scalars().first()

    async def get_user_photo(
            self,
            user_id: int,
            session: AsyncSession
    ):
        _user = await session.execute(
            select(User).where(
                User.id == user_id
            ).options(
                selectinload(User.profile)
            )
        )
        _user = _user.scalars().first()
        image: str = _user.profile.image
        return FileResponse(
            f'{settings.base_dir}/{settings.media_url}{image}'
        )

    async def create(
            self, obj_in: ProfileCreate,
            session: AsyncSession
    ):
        obj_in_data: dict = obj_in.model_dump()
        db_obj = Profile(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_users_obj(
            self,
            user_id: int,
            session: AsyncSession
    ):
        db_obj = await session.execute(
            select(self.model)
            .where(self.model.user_id == user_id)
            .options(
                selectinload(self.model.achievements)
            )
        )
        return db_obj.scalars().first()

    async def update_photo(
            self,
            user_id: int,
            image_url: str,
            session: AsyncSession
    ):
        profile = await session.execute(
            select(Profile)
            .where(
                Profile.user_id == user_id
            )
        )
        profile = profile.scalars().first()
        profile.image = image_url
        session.add(profile)
        await session.commit()
        await session.refresh(profile)
        return profile


profile_crud = CRUDProfile(Profile)
