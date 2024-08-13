from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Question

from .fixtures.question import TEST_QUESTION_COUNT
from .utils import get_obj_count


class TestGetQuestion:
    async def test_get_questions_nonauth(
            self,
            moc_questions,
            db_session: AsyncSession,
            new_client: TestClient
    ):
        """Тест получения всех часто задаваемых вопросов."""
        questions_count = await get_obj_count(Question, db_session)
        response = await new_client.get('/questions/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == questions_count

    async def test_get_question_by_id(
            self,
            moc_questions,
            db_session: AsyncSession,
            new_client: TestClient
    ):
        """Тест полученя часто задаваемого вопроса по id."""
        stmt = select(Question).where(Question.id == 1)
        question = await db_session.execute(stmt)
        question = question.scalar()
        response = await new_client.get('/questions/1')
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result['id'] == question.id

    async def test_get_question_by_nonexist_id(
        self,
        moc_questions,
        db_session: AsyncSession,
        new_client: TestClient
    ):
        """Тест полученя вопроса по несуществующему id."""
        stmt = select(Question).where(Question.id == TEST_QUESTION_COUNT + 1)
        question = await db_session.execute(stmt)
        question = question.scalar()
        response = await new_client.get(
            f'/questions/{TEST_QUESTION_COUNT + 1}'
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestCreateQuestion:
    async def test_method_not_allowed_create_question_nonauth(
            self,
            moc_questions,
            new_client: TestClient
    ):
        """Тест невозможности создания вопроса неавторизованным."""
        response = await new_client.post('/questions/1')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    async def test_method_not_allowed_create_question_user(
            self,
            moc_questions,
            auth_client: TestClient
    ):
        """Тест невозможности создания вопроса юзером."""
        response = await auth_client.post('/questions/1')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    async def test_method_not_allowed_create_question_superuser(
            self,
            moc_questions,
            auth_superuser: TestClient
    ):
        """Тест невозможности создания тарифа суперюзером."""
        response = await auth_superuser.post('/questions/1')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestUpdateQuestion:
    async def test_method_not_allowed_update_question_nonauth(
            self,
            moc_questions,
            new_client: TestClient
    ):
        """Тест невозможности апдейта вопроса неавторизованным."""
        response = await new_client.patch('/questions/1')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    async def test_method_not_allowed_update_question_user(
            self,
            moc_questions,
            auth_client: TestClient
    ):
        """Тест невозможности апдейта вопроса юзером."""
        response = await auth_client.patch('/questions/1')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    async def test_method_not_allowed_update_question_superuser(
            self,
            moc_questions,
            auth_superuser: TestClient
    ):
        """Тест невозможности апдейта тарифа суперюзером."""
        response = await auth_superuser.patch('/questions/1')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestDeleteQuestion:
    async def test_method_not_allowed_delete_question_nonauth(
            self,
            moc_questions,
            new_client: TestClient
    ):
        """Тест невозможности удаления вопроса неавторизованным."""
        response = await new_client.delete('/questions/1')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    async def test_method_not_allowed_delete_question_user(
            self,
            moc_questions,
            auth_client: TestClient
    ):
        """Тест невозможности удаления вопроса юзером."""
        response = await auth_client.delete('/questions/1')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    async def test_method_not_allowed_delete_question_superuser(
        self,
        moc_questions,
        auth_superuser: TestClient
    ):
        """Тест невозможности удаления вопроса суперюзером."""
        response = await auth_superuser.delete('/questions/1')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
