import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Tariff

TEST_TARIFF_COUNT = 6


@pytest_asyncio.fixture
async def moc_tariffs(
    db_session: AsyncSession
) -> None:
    moc_tariffs = [
        Tariff(
            name=f'Tariff_{i}',
            description=f'Description of Tariff_{i}'
        ) for i in range(TEST_TARIFF_COUNT)
    ]
    db_session.add_all(moc_tariffs)
    await db_session.commit()
