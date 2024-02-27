from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_obj_count(
        model,
        session: AsyncSession
) -> int:
    """Возвращает количество объектов в базе."""
    stmt = func.count(model.id)
    count = await session.execute(stmt)
    return count.scalar()


async def get_obj_by_id(
        index: int,
        model,
        session: AsyncSession
) -> Any | None:
    """Возвращает объект по id."""
    stmt = select(model).where(model.id == index)
    obj = await session.execute(stmt)
    return obj.scalar()
