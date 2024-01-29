import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Group


@pytest_asyncio.fixture
async def moc_groups(
    db_session: AsyncSession
) -> None:
    moc_groups = [
        Group(
            name=f'Group_{i}',
            description=f'Description for Group_{i}'
        ) for i in range(1, 6)
    ]
    db_session.add_all(moc_groups)
    await db_session.commit()
