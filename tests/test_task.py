from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Task

from .utils import get_obj_count, get_obj_by_id

CREATE_SCHEME = {
    'name': 'Task name',
    'description': 'Task description'
}
WRONG_CREATE_SCHEME = {
    'description': 'Task description'
}
UPDATE_SCHEME = {
    'name': 'New name of task'
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
        tasks = await get_obj_count(Task, db_session)
        response = auth_superuser.post(
            '/tasks',
            json=CREATE_SCHEME
        )
        assert response.status_code == status.HTTP_201_CREATED
        check_tasks = await get_obj_count(Task, db_session)
        assert check_tasks == tasks + 1

    async def test_wrong_data_create_task(
            self,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест неполных данных для создания таски."""
        tasks = await get_obj_count(Task, db_session)
        response = auth_superuser.post(
            '/tasks',
            json=WRONG_CREATE_SCHEME
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        check_tasks = await get_obj_count(Task, db_session)
        assert check_tasks == tasks

    async def test_create_duplicate_task(
            self,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест запрета создания дубля таски."""
        auth_superuser.post(
            '/tasks',
            json=CREATE_SCHEME
        )
        tasks = await get_obj_count(Task, db_session)
        response = auth_superuser.post(
            '/tasks',
            json=CREATE_SCHEME
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        check_tasks = await get_obj_count(Task, db_session)
        assert check_tasks == tasks


class TestGetTask:
    async def test_forbidden_get_tasks_nonauth(
            self,
            new_client: TestClient
    ):
        """Тест запрета получения таск неавторизованным."""
        response = new_client.get('/tasks')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_forbidden_get_tasks_user(
            self,
            auth_client: TestClient
    ):
        """Тест запрета получения таск юзером."""
        response = auth_client.get('/tasks')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_get_tasks_superuser(
            self,
            moc_tasks,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест получения всех таск."""
        tasks_count = await get_obj_count(Task, db_session)
        response = auth_superuser.get('/tasks')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == tasks_count

    async def test_get_task_by_id_superuser(
            self,
            moc_tasks,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Получение таски по id."""
        response = auth_superuser.get('/tasks/1')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['id'] == 1


class TestUpdateTask:
    async def test_forbidden_update_task_nonauth(
            self,
            new_client: TestClient
    ):
        """Тест запрета апдейта таск неавторизованным."""
        response = new_client.patch('/tasks/1', json=UPDATE_SCHEME)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_forbidden_update_task_user(
            self,
            auth_client: TestClient
    ):
        """Тест запрета апдейта таск юзером."""
        response = auth_client.patch('/tasks/1', json=UPDATE_SCHEME)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_update_task_superuser(
            self,
            moc_tasks,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест апдейта таск."""
        task: Task = await get_obj_by_id(1, Task, db_session)
        response = auth_superuser.patch(
            '/tasks/1',
            json=UPDATE_SCHEME
        )
        assert response.status_code == status.HTTP_200_OK
        check_task: Task = await get_obj_by_id(1, Task, db_session)
        assert check_task.name == UPDATE_SCHEME['name']
        assert check_task.description == task.description


class TestDeleteTask:
    async def test_forbidden_delete_task_nonauth(
            self,
            new_client: TestClient
    ):
        """Тест запрета удаления таск неавторизованным."""
        response = new_client.delete('/tasks/1')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_forbidden_delete_task_user(
            self,
            auth_client: TestClient
    ):
        """Тест запрета удаления таск юзером."""
        response = auth_client.delete('/tasks/1')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_delete_task(
            self,
            moc_tasks,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест удаления таск."""
        tasks_count: int = await get_obj_count(Task, db_session)
        task: Task = await get_obj_by_id(1, Task, db_session)
        assert task.id == 1
        response = auth_superuser.delete('/tasks/1')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        check_tasks_count = await get_obj_count(Task, db_session)
        assert check_tasks_count == tasks_count - 1
        check_task = await get_obj_by_id(1, Task, db_session)
        assert check_task is None
