from typing import Any, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


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
        session: AsyncSession,
        related_objects: Optional[list] = None,
) -> Any | None:
    """Возвращает объект по id."""
    load_related = list()

    if related_objects:
        for obj in related_objects:
            load_related.append(selectinload(obj))

    stmt = select(model).where(model.id == index).options(*load_related)
    obj = await session.execute(stmt)
    return obj.scalar()
