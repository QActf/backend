from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Question
from .fixtures.question import TEST_QUESTION_COUNT
from .utils import get_obj_count

API_QUESTIONS_URL = '/api/questions'
API_QUESTIONS_FIRST_URL = '%s/1' % API_QUESTIONS_URL


class TestQuestion:
    async def test_get_questions_nonauth(
            self,
            new_client: TestClient
    ):
        """Тест получения всех часто задаваемых вопросов неавторизованным."""
        response = await new_client.get(API_QUESTIONS_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_get_questions_user(
            self,
            moc_questions,
            db_session: AsyncSession,
            auth_client: TestClient
    ):
        """Тест получения всех часто задаваемых вопросов."""
        questions_count = await get_obj_count(Question, db_session)
        response = await auth_client.get(API_QUESTIONS_URL)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == questions_count

    async def test_get_question_by_id_nonauth(
            self,
            new_client: TestClient
    ):
        """Тест получения часто задаваемого вопроса по id неавторизованным."""
        response = await new_client.get(API_QUESTIONS_FIRST_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_get_question_by_id_user(
            self,
            moc_questions,
            db_session: AsyncSession,
            auth_client: TestClient
    ):
        """Тест получения часто задаваемого вопроса по id юзером."""
        stmt = select(Question).where(Question.id == 1)
        question = await db_session.execute(stmt)
        question = question.scalar()
        response = await auth_client.get(API_QUESTIONS_FIRST_URL)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result['id'] == question.id

    async def test_get_question_by_nonexist_id(
        self,
        moc_questions,
        db_session: AsyncSession,
        auth_client: TestClient
    ):
        """Тест полученя вопроса по несуществующему id юзером."""
        stmt = select(Question).where(Question.id == TEST_QUESTION_COUNT + 1)
        question = await db_session.execute(stmt)
        question = question.scalar()
        response = await auth_client.get(
            f'{API_QUESTIONS_URL}/{TEST_QUESTION_COUNT + 1}'
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_method_not_allowed_create_question_user(
            self,
            auth_client: TestClient
    ):
        """Тест невозможности создания вопроса юзером."""
        response = await auth_client.post(API_QUESTIONS_FIRST_URL)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    async def test_method_not_allowed_update_question(
            self,
            auth_client: TestClient
    ):
        """Тест невозможности апдейта вопроса юзером."""
        response = await auth_client.patch(API_QUESTIONS_FIRST_URL)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    async def test_method_not_allowed_delete_question_user(
            self,
            auth_client: TestClient
    ):
        """Тест невозможности удаления вопроса юзером."""
        response = await auth_client.delete(API_QUESTIONS_FIRST_URL)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
