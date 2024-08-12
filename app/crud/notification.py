from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Notification
from app.models.notification import notification_user_association


class CRUDNotification(CRUDBase):
    async def add_notification_for_user(
            self,
            obj_in,
            session: AsyncSession,
    ):
        stmt = notification_user_association.insert().values(
            user_id=obj_in.user_id,
            notification_id=obj_in.notification_id,
        )
        await session.execute(stmt)
        await session.commit()

    async def get_user_notifications(
            self,
            user_id: int,
            viewed: bool,
            bell: bool,
            session: AsyncSession,
    ):
        stmt = select(
            self.model.name,
            self.model.message if not bell else None,
            notification_user_association.c.id,
            notification_user_association.c.date,
        ).join(
            notification_user_association,
        ).where(and_(
            notification_user_association.c.user_id == user_id,
            notification_user_association.c.viewed == (
                viewed if not bell else False
            ),
        ))
        db_objs = await session.execute(stmt)
        return db_objs.mappings().all()

    async def get_user_notification_by_id(
            self,
            obj_id: int,
            user_id: int,
            session: AsyncSession,
    ):
        stmt = select(
            notification_user_association,
        ).where(and_(
            notification_user_association.c.id == obj_id,
            notification_user_association.c.user_id == user_id,
        ))
        db_obj = await session.execute(stmt)
        return db_obj.mappings().all()

    async def mark_user_notification_as_viewed(self, obj_id, session):
        stmt = update(
            notification_user_association,
        ).where(
            notification_user_association.c.id == obj_id,
        ).values(viewed=True)
        await session.execute(stmt)
        await session.commit()

    async def remove(self, db_obj: Notification, session: AsyncSession):
        stmt = notification_user_association.delete().where(
            notification_user_association.c.notification_id == db_obj.id
        )
        await session.execute(stmt)
        await session.delete(db_obj)
        await session.commit()


notification_crud = CRUDNotification(Notification)
