from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models import Tariff


class CRUDTariff(CRUDBase):
    async def get_tariff(
            self,
            session: AsyncSession,
            attr_name: Optional[str] = None,
            attr_value: Optional[str] = None,
            courses: bool = False,
            users: bool = False,
            multi: bool = False,
            is_closed: Optional[bool] = None,
    ):
        """Вернет тариф(ы)."""
        stmt = select(self.model)

        conditions = []
        if attr_name and attr_value is not None:
            conditions.append(getattr(self.model, attr_name) == attr_value)
        if is_closed is not None:
            conditions.append(self.model.is_closed == (1 if is_closed
                                                       else None))
        if conditions:
            stmt = stmt.where(and_(*conditions))

        load_related = list()
        if courses:
            load_related.append(selectinload(self.model.courses))
        if users:
            load_related.append(selectinload(self.model.users))
        stmt = stmt.options(*load_related)

        result = await session.execute(stmt)
        return result.scalars().all() if multi else result.scalars().first()

    async def close_tariff(
            self,
            tariff: Tariff,
            session: AsyncSession
    ):
        """Закрытие тарифа по его id."""
        tariff.is_closed = True
        session.add(tariff)
        await session.commit()
        await session.refresh(tariff)
        return tariff


tariff_crud = CRUDTariff(Tariff)
