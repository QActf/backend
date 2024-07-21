from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_obj_exists
from app.models import User


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get_by_attr(
            self,
            attr_name: str,
            attr_value: str,
            session: AsyncSession,
    ):
        """Вернет объект модели по значению указанного атрибута."""
        db_obj = await session.execute(
            select(self.model).where(
                getattr(self.model, attr_name) == attr_value
            )
        )
        obj = db_obj.scalars().first()
        return obj

    async def get_multi(self, session: AsyncSession):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def get_users_obj(
        self,
        user_id: int,
        session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(self.model.user_id == user_id)
        )
        return db_obj.scalars().all()

    async def create(
            self, obj_in, session: AsyncSession, user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj
