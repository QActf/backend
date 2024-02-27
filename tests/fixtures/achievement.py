import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Achievement


@pytest_asyncio.fixture
async def moc_achievements(
    db_session: AsyncSession
) -> None:
    moc_achievements = [
        Achievement(
            name=f'Achievement_{i}',
            description=f'Description for Achievemetnt_{i}'
        ) for i in range(1, 6)
    ]
    db_session.add_all(moc_achievements)
    await db_session.commit()
