import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Question

TEST_QUESTION_COUNT = 6


@pytest_asyncio.fixture
async def moc_questions(
    db_session: AsyncSession
) -> None:
    moc_questions = [
        Question(
            problem=f'Problem_{i}',
            solution=f'Solution of Problem_{i}'
        ) for i in range(TEST_QUESTION_COUNT)
    ]
    db_session.add_all(moc_questions)
    await db_session.commit()
