from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models import Profile
from app.schemas.profile import ProfileCreate


class CRUDProfile(CRUDBase):

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
        setattr(profile, 'image', image_url)
        session.add(profile)
        await session.commit()
        await session.refresh(profile)
        return profile


profile_crud = CRUDProfile(Profile)
