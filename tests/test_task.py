from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from app.models import Task

CREATE_SCHEME = {
    'name': 'Task name',
    'description': 'Task description'
}
WRONG_CREATE_SCHEME = {
    'description': 'Task description'
}


class TestCreateTask:
    async def test_forbidden_create_task_nonauth(
            self,
            new_client: TestClient
    ):
        """Тест запрета создания таск неавторизованным."""
        response = new_client.post('/tasks')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_forbidden_create_task_user(
            self,
            auth_client: TestClient
    ):
        """Тест запрета создания таск юзером."""
        response = auth_client.post('/tasks')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_create_task(
            self,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест создания таски."""
        stmt = func.count(Task.id)
        tasks = await db_session.execute(stmt)
        tasks = tasks.scalar()
        response = auth_superuser.post(
            '/tasks',
            json=CREATE_SCHEME
        )
        assert response.status_code == status.HTTP_201_CREATED
        check_tasks = await db_session.execute(stmt)
        check_tasks = check_tasks.scalar()
        assert check_tasks == tasks + 1

    async def test_wrong_data_create_task(
            self,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест неполных данных для создания таски."""
        stmt = func.count(Task.id)
        tasks = await db_session.execute(stmt)
        tasks = tasks.scalar()
        response = auth_superuser.post(
            '/tasks',
            json=WRONG_CREATE_SCHEME
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        check_tasks = await db_session.execute(stmt)
        check_tasks = check_tasks.scalar()
        assert check_tasks == tasks


class TestGetTask:
    ...


class TestUpdateTask:
    ...


class TestDeleteTask:
    ...
