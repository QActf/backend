from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Task
from app.models.task import tasks_solved_user_association


class CRUDTask(CRUDBase):

    async def get_task_done_user_association(
            self,
            user_id: int,
            task_id: int,
            session: AsyncSession,
    ):
        """Вернет ассоциацию решенная-задача - пользователь."""
        stmt = select(tasks_solved_user_association).where(
            and_(
                tasks_solved_user_association.c.user_id == user_id,
                tasks_solved_user_association.c.task_id == task_id
            )
        )
        obj = await session.execute(stmt)
        return obj.scalars().first()

    async def create_task_done_user_association(
            self,
            obj_in,
            session: AsyncSession,
    ):
        """Создаст запись о том, что пользователь решил задачу."""
        stmt = tasks_solved_user_association.insert().values(
            user_id=obj_in.user_id,
            task_id=obj_in.task_id,
        )
        await session.execute(stmt)
        await session.commit()


task_crud = CRUDTask(Task)
