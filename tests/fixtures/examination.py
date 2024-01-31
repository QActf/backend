import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Examination


@pytest_asyncio.fixture
async def moc_examinations(
    db_session: AsyncSession
) -> None:
    moc_examinations = [
        Examination(
            name=f'Examination_{i}',
            description=f'Description of Examination_{i}'
        ) for i in range(1, 6)
    ]
    db_session.add_all(moc_examinations)
    await db_session.commit()
