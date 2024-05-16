from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Examination, User

from .utils import get_obj_by_id, get_obj_count

CREATE_SCHEME = {
    'name': 'Examination name',
    'description': 'Examination description'
}
WRONG_CREATE_SCHEME = {
    'description': 'Examination description'
}
UPDATE_SCHEME = {
    'name': 'New Examination name',
}


async def _get_examination_by_id_with_relation_user(
        index: int,
        session: AsyncSession
):
    stmt = (
        select(Examination)
        .where(Examination.id == index)
        .options(
            selectinload(Examination.users)
        )
    )
    examination = await session.execute(stmt)
    return examination.scalar()


class TestCreateExamination:
    async def test_create_examination_forbidden_nonauth(
        self,
        new_client: TestClient
    ):
        """Тест запрета создания экзамена неавторизованным."""
        response = await new_client.post('/examinations/', json=CREATE_SCHEME)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_create_examination_forbidden_user(
        self,
        auth_client: TestClient
    ):
        """Тест запрета создания экзамена юзером."""
        response = await auth_client.post('/examinations/', json=CREATE_SCHEME)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_create_examination_superuser(
        self,
        db_session: AsyncSession,
        auth_superuser: TestClient
    ):
        """Тест создания экзамена."""
        examinations_count = await get_obj_count(Examination, db_session)
        response = await auth_superuser.post(
            '/examinations/', json=CREATE_SCHEME
        )
        assert response.status_code == status.HTTP_201_CREATED
        check_examinations_count = await get_obj_count(Examination, db_session)
        assert check_examinations_count == examinations_count + 1

    async def test_create_examination_wrong_data(
            self,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест неправильных данных создания экзамена."""
        examinations_count = await get_obj_count(Examination, db_session)
        response = await auth_superuser.post(
            '/examinations/', json=WRONG_CREATE_SCHEME
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        check_examinations_count = await get_obj_count(Examination, db_session)
        assert check_examinations_count == examinations_count

    async def test_create_examination_duplicate_forbidden(
            self,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест запрета создания дубля экзамена."""
        await auth_superuser.post('/examinations/', json=CREATE_SCHEME)
        examinations_count = await get_obj_count(Examination, db_session)
        response = await auth_superuser.post(
            '/examinations/', json=CREATE_SCHEME
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        check_examinations_count = await get_obj_count(Examination, db_session)
        assert check_examinations_count == examinations_count


class TestGetExamination:
    async def test_get_all_examinations(
            self,
            moc_examinations,
            db_session: AsyncSession,
            new_client: TestClient
    ):
        """Тест получения всех экзаменов."""
        examinations_count = await get_obj_count(Examination, db_session)
        response = await new_client.get('/examinations/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == examinations_count

    async def test_get_examination_by_id(
            self,
            moc_examinations,
            db_session: AsyncSession,
            new_client: TestClient
    ):
        """Тест получения экзамена по id."""
        response = new_client.get('/examinations/1')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        # response = await new_client.get('/examinations/1')
        # assert response.status_code == status.HTTP_200_OK
        # assert response.json()['id'] == 1
        # response = await new_client.get('/examinations/100')
        # assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_self_examinations_user(
            self,
            moc_examinations,
            register_client,
            db_session: AsyncSession,
            auth_client: TestClient
    ):
        """Тест получения списка своих экзаменов юзером."""
        examination_1 = await _get_examination_by_id_with_relation_user(
            1, db_session
        )
        examination_2 = await _get_examination_by_id_with_relation_user(
            2, db_session
        )
        user = await get_obj_by_id(register_client.id, User, db_session)
        examination_1.users.append(user)
        examination_2.users.append(user)
        await db_session.commit()
        response = await auth_client.get('/examinations/me')
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert len(result) == 2
        assert result[0]['id'] in (1, 2)
        assert result[1]['id'] in (1, 2)
        assert result[0]['id'] != result[1]['id']


class TestUpdateExamination:
    async def test_update_examination_forbidden_nonauth(
        self,
        new_client: TestClient
    ):
        """Тест запрета апдейта экзамена неавторизованным."""
        response = await new_client.patch(
            '/examinations/1', json=UPDATE_SCHEME
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_update_examination_forbidden_user(
        self,
        auth_client: TestClient
    ):
        """Тест запрета апдейта экзамена юзером."""
        response = await auth_client.patch(
            '/examinations/1', json=UPDATE_SCHEME
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_update_examination_superuser(
            self,
            moc_examinations,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест апдейта экзамена."""
        examination: Examination = await get_obj_by_id(
            1, Examination, db_session
        )
        response = await auth_superuser.patch(
            '/examinations/1', json=UPDATE_SCHEME
        )
        assert response.status_code == status.HTTP_200_OK
        check_examination: Examination = await get_obj_by_id(
            1, Examination, db_session
        )
        assert check_examination.name == UPDATE_SCHEME['name']
        assert check_examination.description == examination.description


class TestDeleteExamination:
    async def test_delete_examination_forbidden_nonauth(
        self,
        moc_examinations,
        db_session: AsyncSession,
        new_client: TestClient
    ):
        """Тест запрета удаления экзамена неавторизованным."""
        examinations_count = await get_obj_count(Examination, db_session)
        response = await new_client.delete('/examinations/1')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        check_examinations_count = await get_obj_count(Examination, db_session)
        assert check_examinations_count == examinations_count

    async def test_delete_examination_forbidden_user(
        self,
        moc_examinations,
        db_session: AsyncSession,
        auth_client: TestClient
    ):
        """Тест запрета удаления экзамена юзером."""
        examinations_count = await get_obj_count(Examination, db_session)
        response = await auth_client.delete('/examinations/1')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        check_examinations_count = await get_obj_count(Examination, db_session)
        assert check_examinations_count == examinations_count

    async def test_delete_examination(
        self,
        moc_examinations,
        db_session: AsyncSession,
        auth_superuser: TestClient
    ):
        """Тест удаления экзамена."""
        examinations_count = await get_obj_count(Examination, db_session)
        examination = await get_obj_by_id(1, Examination, db_session)
        assert examination.id == 1
        response = await auth_superuser.delete('/examinations/1')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        check_examinations_count = await get_obj_count(Examination, db_session)
        assert check_examinations_count == examinations_count - 1
        examination = await get_obj_by_id(1, Examination, db_session)
        assert examination is None
