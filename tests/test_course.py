from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import Course, User

from .utils import get_obj_count, get_obj_by_id


CREATE_SCHEME = {
    'name': 'Course name',
    'description': 'Course description'
}
WRONG_CREATE_SCHEME = {
    'description': 'Course description'
}
UPDATE_SCHEME = {
    'name': 'New Course name',
}


async def _get_course_by_id_with_relation_user(
        index: int,
        session: AsyncSession
):
    stmt = (
        select(Course)
        .where(Course.id == index)
        .options(
            selectinload(Course.users)
        )
    )
    course = await session.execute(stmt)
    return course.scalar()


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
    async def test_get_all_courses(
            self,
            moc_courses,
            db_session: AsyncSession,
            new_client: TestClient
    ):
        """Тест получения всех курсов."""
        courses_count = await get_obj_count(Course, db_session)
        response = new_client.get('/courses')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == courses_count

    async def test_get_course_by_id(
            self,
            moc_courses,
            db_session: AsyncSession,
            new_client: TestClient
    ):
        """Тест получения курса по id."""
        response = new_client.get('/courses/1')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['id'] == 1
        response = new_client.get('/courses/100')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_self_courses_user(
            self,
            moc_courses,
            register_client,
            db_session: AsyncSession,
            auth_client: TestClient
    ):
        """Тест получения списка своих курсов юзером."""
        course_1 = await _get_course_by_id_with_relation_user(1, db_session)
        course_2 = await _get_course_by_id_with_relation_user(2, db_session)
        user = await get_obj_by_id(register_client.id, User, db_session)
        course_1.users.append(user)
        course_2.users.append(user)
        await db_session.commit()
        response = auth_client.get('/courses/me')
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert len(result) == 2
        assert result[0]['id'] in (1, 2)
        assert result[1]['id'] in (1, 2)
        assert result[0]['id'] != result[1]['id']


class TestUpdateCourse:
    async def test_update_course_forbidden_nonauth(
        self,
        new_client: TestClient
    ):
        """Тест запрета апдейта курса неавторизованным."""
        response = new_client.patch('/courses/1', json=UPDATE_SCHEME)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_update_course_forbidden_user(
        self,
        auth_client: TestClient
    ):
        """Тест запрета апдейта курса юзером."""
        response = auth_client.patch('/courses/1', json=UPDATE_SCHEME)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_update_course_superuser(
            self,
            moc_courses,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест апдейта курса."""
        course: Course = await get_obj_by_id(1, Course, db_session)
        response = auth_superuser.patch(
            '/courses/1', json=UPDATE_SCHEME
        )
        assert response.status_code == status.HTTP_200_OK
        check_course: Course = await get_obj_by_id(1, Course, db_session)
        assert check_course.name == UPDATE_SCHEME['name']
        assert check_course.description == course.description


class TestDeleteCourse:
    async def test_delete_course_forbidden_nonauth(
        self,
        moc_courses,
        db_session: AsyncSession,
        new_client: TestClient
    ):
        """Тест запрета удаления курса неавторизованным."""
        courses_count = await get_obj_count(Course, db_session)
        response = new_client.delete('/courses/1')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        check_courses_count = await get_obj_count(Course, db_session)
        assert check_courses_count == courses_count

    async def test_delete_course_forbidden_user(
        self,
        moc_courses,
        db_session: AsyncSession,
        auth_client: TestClient
    ):
        """Тест запрета удаления курса юзером."""
        courses_count = await get_obj_count(Course, db_session)
        response = auth_client.delete('/courses/1')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        check_courses_count = await get_obj_count(Course, db_session)
        assert check_courses_count == courses_count

    async def test_delete_course(
        self,
        moc_courses,
        db_session: AsyncSession,
        auth_superuser: TestClient
    ):
        """Тест удаления курса."""
        courses_count = await get_obj_count(Course, db_session)
        course = await get_obj_by_id(1, Course, db_session)
        assert course.id == 1
        response = auth_superuser.delete('/courses/1')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        check_courses_count = await get_obj_count(Course, db_session)
        assert check_courses_count == courses_count - 1
        course = await get_obj_by_id(1, Course, db_session)
        assert course is None
