from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models import Group, User
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class CRUDGroup(CRUDBase):
    async def get_users_obj(self, user_id: int, session: AsyncSession):
        stmt = (
            select(Group)
            # .where(Group.users == user_id)
            .options(
                selectinload(Group.users)
            ).where(Group.users.any(User.id == user_id))
        )
        db_obj = await session.execute(stmt)
        return db_obj.scalars().all()


group_crud = CRUDGroup(Group)
