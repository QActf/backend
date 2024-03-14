from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models import Group, User


class CRUDGroup(CRUDBase):
    async def get(self, group_id: int, session: AsyncSession):
        stmt = (
            select(Group)
            .where(Group.id == group_id)
            .options(
                selectinload(Group.users)
            )
        )
        group = await session.execute(stmt)
        group = group.scalars().first()
        return group

    async def get_users_obj(self, user_id: int, session: AsyncSession):
        stmt = (
            select(Group)
            .options(
                selectinload(Group.users)
            ).where(Group.users.any(User.id == user_id))
        )
        db_obj = await session.execute(stmt)
        return db_obj.scalars().all()


group_crud = CRUDGroup(Group)
