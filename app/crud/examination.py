from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models import Examination, User


class CRUDExamination(CRUDBase):
    async def get_users_obj(self, user_id: int, session: AsyncSession):
        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.users)
            ).where(self.model.users.any(User.id == user_id))
        )
        db_obj = await session.execute(stmt)
        return db_obj.scalars().all()


examination_crud = CRUDExamination(Examination)
