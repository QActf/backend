import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Task


@pytest_asyncio.fixture
async def moc_tasks(
    db_session: AsyncSession
) -> None:
    moc_tasks = [
        Task(
            name=f'Task_{i}',
            description=f'Description of Task_{i}'
        ) for i in range(1, 6)
    ]
    db_session.add_all(moc_tasks)
    await db_session.commit()
