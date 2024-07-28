from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models import ContactInformationBlock
from app.models.user import User


class CRUDContactInformationBlock(CRUDBase):

    async def create(
        self, obj_in, session: AsyncSession, user: User | None = None
    ):
        if await self.get_multi(session):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=('Контакты уже существуют. Если надо изменить контакты '
                        'воспользуйтесь методом PATCH.')
            )
        return await super().create(obj_in, session, user)

    async def get_contact_info(self, session: AsyncSession):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().first()


contact_info_crud = CRUDContactInformationBlock(ContactInformationBlock)
