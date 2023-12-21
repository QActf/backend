from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models import Profile
from app.schemas.profile import ProfileCreate


class CRUDProfile(CRUDBase):

    async def create(
            self, obj_in: ProfileCreate,
            user_id: int, session: AsyncSession
    ):
        obj_in_data: dict = obj_in.model_dump()
        obj_in_data['user_id'] = user_id
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


profile_crud = CRUDProfile(Profile)
