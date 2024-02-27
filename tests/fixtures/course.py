import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Course


@pytest_asyncio.fixture
async def moc_courses(
    db_session: AsyncSession
) -> None:
    moc_courses = [
        Course(
            name=f'Course_{i}',
            description=f'Description of Course_{i}'
        ) for i in range(1, 6)
    ]
    db_session.add_all(moc_courses)
    await db_session.commit()
