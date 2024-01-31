from app.crud.base import CRUDBase
from app.models import Course, User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class CRUDCourse(CRUDBase):
    async def get_users_obj(self, user_id: int, session: AsyncSession):
        stmt = (
            select(Course)
            .options(
                selectinload(Course.users)
            ).where(Course.users.any(User.id == user_id))
        )
        db_obj = await session.execute(stmt)
        return db_obj.scalars().all()


course_crud = CRUDCourse(Course)
