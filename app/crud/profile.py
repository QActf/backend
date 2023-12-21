from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Profile
from app.schemas.profile import ProfileCreate


class CRUDProfile(CRUDBase):
    async def create(
            self, obj_in: ProfileCreate, user_id: int, session: AsyncSession
    ):
        obj_in_data: dict = obj_in.model_dump()
        obj_in_data["user_id"] = user_id
        db_obj = Profile(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


profile_crud = CRUDProfile(Profile)
