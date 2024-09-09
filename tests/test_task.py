from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Task
from .utils import get_obj_by_id, get_obj_count

API_TASKS_URL = '/api/tasks/'
API_TASKS_FIRST_URL = '%s1' % API_TASKS_URL

CREATE_SCHEME = {
    'name': 'Task name',
    'description': 'Task description',
    'difficult': 5
}
WRONG_CREATE_SCHEME = {
    'description': 'Task description'
}
UPDATE_NAME_SCHEME = {
    'name': 'New name of task'
}
UPDATE_DIFFICULT_SCHEME = {
    'difficult': 10
}


class TestCreateTask:
    async def test_forbidden_create_task_nonauth(
            self,
            new_client: TestClient
    ):
        """Тест запрета создания таск неавторизованным."""
        response = await new_client.post(API_TASKS_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_forbidden_create_task_user(
            self,
            auth_client: TestClient
    ):
        """Тест запрета создания таск юзером."""
        response = await auth_client.post(API_TASKS_URL)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_create_task(
            self,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест создания таски."""
        tasks = await get_obj_count(Task, db_session)
        response = await auth_superuser.post(
            API_TASKS_URL,
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
        response = await auth_superuser.post(
            API_TASKS_URL,
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
        await auth_superuser.post(
            API_TASKS_URL,
            json=CREATE_SCHEME
        )
        tasks = await get_obj_count(Task, db_session)
        response = await auth_superuser.post(
            API_TASKS_URL,
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
        response = await new_client.get(API_TASKS_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_forbidden_get_tasks_user(
            self,
            auth_client: TestClient
    ):
        """Тест запрета получения таск юзером."""
        response = await auth_client.get(API_TASKS_URL)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_get_tasks_superuser(
            self,
            moc_tasks,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест получения всех таск суперюзером."""
        tasks_count = await get_obj_count(Task, db_session)
        response = await auth_superuser.get(API_TASKS_URL)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == tasks_count

    async def test_get_task_by_id_superuser(
            self,
            moc_tasks,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Получение таски по id."""
        response = await auth_superuser.get(API_TASKS_FIRST_URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['key'] == 1


class TestUpdateTask:
    async def test_forbidden_update_task_nonauth(
            self,
            new_client: TestClient
    ):
        """Тест запрета апдейта таск неавторизованным."""
        response = await new_client.patch(API_TASKS_FIRST_URL, json=UPDATE_NAME_SCHEME)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_forbidden_update_task_user(
            self,
            auth_client: TestClient
    ):
        """Тест запрета апдейта таск юзером."""
        response = await auth_client.patch(API_TASKS_FIRST_URL, json=UPDATE_NAME_SCHEME)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_update_task_superuser(
            self,
            moc_tasks,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест апдейта таск."""
        task: Task = await get_obj_by_id(1, Task, db_session)
        response = await auth_superuser.patch(
            API_TASKS_FIRST_URL,
            json=UPDATE_NAME_SCHEME
        )
        assert response.status_code == status.HTTP_200_OK
        check_task: Task = await get_obj_by_id(1, Task, db_session)
        assert check_task.name == UPDATE_NAME_SCHEME['name']
        assert check_task.description == task.description

    async def test_update_wrong_difficult_task(
            self,
            moc_tasks,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест апдейта таски с неверной сложностью."""
        task: Task = await get_obj_by_id(1, Task, db_session)
        response = await auth_superuser.patch(
            API_TASKS_FIRST_URL,
            json=UPDATE_DIFFICULT_SCHEME
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        check_task: Task = await get_obj_by_id(1, Task, db_session)
        assert check_task == task


class TestDeleteTask:
    async def test_forbidden_delete_task_nonauth(
            self,
            new_client: TestClient
    ):
        """Тест запрета удаления таск неавторизованным."""
        response = await new_client.delete(API_TASKS_FIRST_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_forbidden_delete_task_user(
            self,
            auth_client: TestClient
    ):
        """Тест запрета удаления таск юзером."""
        response = await auth_client.delete(API_TASKS_FIRST_URL)
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
        response = await auth_superuser.delete(API_TASKS_FIRST_URL)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        check_tasks_count = await get_obj_count(Task, db_session)
        assert check_tasks_count == tasks_count - 1
        check_task = await get_obj_by_id(1, Task, db_session)
        assert check_task is None
