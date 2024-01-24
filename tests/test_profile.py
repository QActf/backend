from typing import AsyncGenerator

from fastapi import status, Response
from fastapi.testclient import TestClient
from sqlalchemy import select

from tests.fixtures.user import USER_EMAIL, USER_PASSWORD, USER_USERNAME
from tests.conftest import AsyncSessionLocalTest

from app.crud.profile import profile_crud
from app.crud.user import user_crud
from app.models import Profile, User

REGISTRATION_SCHEMA = {
    'email': USER_EMAIL,
    'password': USER_PASSWORD,
    'role': 'user',
    'username': USER_USERNAME,
}


class TestCreateProfile:
    async def test_create_profile_with_create_user(
            self, new_client, db_session
    ):
        """Тест создания профиля при регистрации пользователя."""
        profiles = await profile_crud.get_multi(db_session)
        assert len(profiles) == 0
        users = await user_crud.get_multi(db_session)
        assert len(users) == 0
        response: Response = new_client.post(
            '/auth/register', json=REGISTRATION_SCHEMA
        )
        assert response.status_code == status.HTTP_201_CREATED
        profiles = await profile_crud.get_multi(db_session)
        assert len(profiles) == 1
        users = await user_crud.get_multi(db_session)
        assert len(users) == 1


class TestSuperuser:
    async def test_get_all_profiles_superuser(
            self,
            moc_users,
            db_session: AsyncGenerator,
            auth_superuser: AsyncGenerator | TestClient
    ):
        """Тест получения всех профилей суперюзером."""
        profiles = await profile_crud.get_multi(db_session)
        response: Response = auth_superuser.get(
            '/profiles/'
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == len(profiles)

    async def test_forbidden_get_all_profiles_for_user(
            self,
            moc_users,
            db_session: AsyncGenerator,
            auth_client: AsyncGenerator | TestClient,
    ):
        """Тест запрета получения профилей простым пользователем."""
        response = auth_client.get(
            '/profiles/'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_filter_profiles(
            self,
            moc_users,
            db_session,
            auth_superuser
    ):
        """Тест фильтрации профилей."""
        # stmt = select(User).filter(User.username.ilike('%user%'))
        # users = await db_session.execute(stmt)
        # users = users.scalars().all()
        # print(users)
        # profiles = await profile_crud.get_multi(db_session)
        # print(profiles)
        response = auth_superuser.get(
            '/profiles/?age__gte=22&age__lte=23'
        )
        assert len(response.json()) == 2
        response = auth_superuser.get(
            '/profiles/?first_name__ilike=3'
        )
        assert len(response.json()) == 1
        response = auth_superuser.get(
            '/profiles/?last_name__ilike=4'
        )
        assert len(response.json()) == 1

    async def test_pagination(
            self,
            moc_users,
            auth_superuser
    ):
        """Тест пагинации профилей"""
        response = auth_superuser.get(
            '/profiles/?limit=2'
        )
        result = response.json()
        assert len(result) == 2
        assert result[0]['user_id'] == 1
        assert result[1]['user_id'] == 2
        response = auth_superuser.get(
            '/profiles/?offset=2&limit=2'
        )
        result = response.json()
        assert len(result) == 2
        assert result[0]['user_id'] == 3
        assert result[1]['user_id'] == 4

    async def test_6(self):
        """Тест получения своего профиля текущим юзером."""
        ...

    async def test_7(self):
        """Тест запрета получения чужого профиля текущим юзером."""
        ...

    async def test_8(self):
        """Тест получения фото своего профиля юзером."""
        ...

    async def test_9(self):
        """Тест запрета получения фото чужого профиля."""
        ...

    async def test_10(self):
        """Тест апдейта своего профиля."""
        ...

    async def test_11(self):
        """Тест запрета апдейта чужого профиля."""
        ...

    async def test_12(self):
        """Тест апдейта фото своего профиля."""
        ...

    async def test_13(self):
        """Тест запрета апдейта фото чужого профиля."""
        ...

    async def test_14(self):
        """Тест запрета создания профиля без создания юзера."""
        ...

    # async def test_forbidden_delete_profile(
    #         self,
    #         user_1,
    #         db_session,
    #         auth_superuser: AsyncGenerator | TestClient
    # ):
    #     """Тест запрета удаления профиля."""
    #     users = await user_crud.get_multi(db_session)
    #     user: User = users[0]
    #     profile: Profile = await profile_crud.get_users_obj(user.id, db_session)
    #     response = auth_superuser.delete(
    #         f'/profiles/{profile.id}/'
    #     )
    #     assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
