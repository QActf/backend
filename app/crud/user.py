from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import User


class CRUDUser(CRUDBase):

    async def update_id(
        self,
        db_obj,
        field: str,
        field_value: int,
        session: AsyncSession,
    ):
        # obj_data = jsonable_encoder(db_obj)
        setattr(db_obj, field, field_value)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


user_crud = CRUDUser(User)
