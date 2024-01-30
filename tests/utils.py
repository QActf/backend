from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession


async def get_obj_count(
        model,
        session: AsyncSession
) -> int:
    """Возвращает количество объектов в базе."""
    stmt = func.count(model.id)
    count = await session.execute(stmt)
    return count.scalar()
