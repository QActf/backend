from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Course

from .utils import get_obj_count


CREATE_SCHEME = {
    'name': 'Course name',
    'description': 'Course description'
}
WRONG_CREATE_SCHEME = {
    'description': 'Course description'
}


class TestCreateCourse:
    async def test_create_course_forbidden_nonauth(
        self,
        new_client: TestClient
    ):
        """Тест запрета создания курса неавторизованным."""
        response = new_client.post('/courses', json=CREATE_SCHEME)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_create_course_forbidden_user(
        self,
        auth_client: TestClient
    ):
        """Тест запрета создания курса юзером."""
        response = auth_client.post('/courses', json=CREATE_SCHEME)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_create_course_superuser(
        self,
        db_session: AsyncSession,
        auth_superuser: TestClient
    ):
        """Тест создания курса."""
        courses_count = await get_obj_count(Course, db_session)
        response = auth_superuser.post('/courses', json=CREATE_SCHEME)
        assert response.status_code == status.HTTP_201_CREATED
        check_courses_count = await get_obj_count(Course, db_session)
        assert check_courses_count == courses_count + 1

    async def test_create_course_wrong_data(
            self,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест неправильных данных создания курса."""
        courses_count = await get_obj_count(Course, db_session)
        response = auth_superuser.post('/courses', json=WRONG_CREATE_SCHEME)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        check_courses_count = await get_obj_count(Course, db_session)
        assert check_courses_count == courses_count

    async def test_create_course_duplicate_forbidden(
            self,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест запрета создания дубля курса."""
        auth_superuser.post('/courses', json=CREATE_SCHEME)
        courses_count = await get_obj_count(Course, db_session)
        response = auth_superuser.post('/courses', json=CREATE_SCHEME)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        check_courses_count = await get_obj_count(Course, db_session)
        assert check_courses_count == courses_count


class TestGetCourse:
    ...


class TestUpdateCourse:
    ...


class TestDeleteCourse:
    ...
