import base64
import io
import pytest
from pathlib import Path
from typing import AsyncGenerator

from fastapi import Response, status
from fastapi.testclient import TestClient
from PIL import Image
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.models import Profile, User
from tests.fixtures.user import USER_EMAIL, USER_PASSWORD, USER_USERNAME

from .utils import get_obj_count

REGISTRATION_SCHEMA = {
    'email': USER_EMAIL,
    'password': USER_PASSWORD,
    'role': 'user',
    'username': USER_USERNAME,
}


def delete_tmpdir(path: Path):
    for sub in path.iterdir():
        if sub.is_dir():
            delete_tmpdir(sub)
        else:
            sub.unlink()
    path.rmdir()


async def _get_user(
        user_id: int,
        db_session,
):
    user = await db_session.execute(
        select(User).filter(User.id == user_id)
        .options(selectinload(User.profile))
    )
    user: User = user.scalars().first()
    return user


class TestProfile:
    @pytest.mark.skip
    async def test_create_profile_with_create_user(
            self, new_client,
            db_session: AsyncSession
    ):
        """Тест создания профиля при регистрации пользователя."""
        profiles = await get_obj_count(Profile, db_session)
        users = await get_obj_count(User, db_session)
        response: Response = await new_client.post(
            '/auth/register', json=REGISTRATION_SCHEMA
        )
        assert response.status_code == status.HTTP_201_CREATED
        check_profiles = await get_obj_count(Profile, db_session)
        assert check_profiles == profiles + 1
        check_users = await get_obj_count(User, db_session)
        assert check_users == users + 1

    async def test_get_all_profiles_superuser(
            self,
            moc_users,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест получения всех профилей суперюзером."""
        profiles = await get_obj_count(Profile, db_session)
        response: Response = await auth_superuser.get(
            '/profiles/'
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == profiles

    async def test_forbidden_get_all_profiles_user(
            self,
            moc_users,
            auth_client: TestClient,
    ):
        """Тест запрета получения профилей простым пользователем."""
        response = await auth_client.get(
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
        response = await auth_superuser.get(
            '/profiles/?age__gte=22&age__lte=23'
        )
        assert len(response.json()) == 2
        response = await auth_superuser.get(
            '/profiles/?first_name__ilike=3'
        )
        assert len(response.json()) == 1
        response = await auth_superuser.get(
            '/profiles/?last_name__ilike=4'
        )
        assert len(response.json()) == 1

    async def test_pagination(
            self,
            moc_users,
            auth_superuser
    ):
        """Тест пагинации профилей"""
        response = await auth_superuser.get(
            '/profiles/?limit=2'
        )
        result = response.json()
        assert len(result) == 2
        assert result[0]['user_id'] == 1
        assert result[1]['user_id'] == 2
        response = await auth_superuser.get(
            '/profiles/?offset=2&limit=2'
        )
        result = response.json()
        assert len(result) == 2
        assert result[0]['user_id'] == 3
        assert result[1]['user_id'] == 4

    async def test_get_self_profile(
            self,
            moc_users,
            new_client,
            db_session
    ):
        """Тест получения своего профиля текущим юзером."""
        user = await _get_user(1, db_session)
        response: Response = await new_client.post(
           '/auth/jwt/login',
           data={'username': user.email, 'password': 'qwerty'},
        )
        access_token = response.json().get('access_token')
        new_client.headers.update({'Authorization': f'Bearer {access_token}'})
        response: Response = await new_client.get(
            '/profiles/me'
        )
        result = response.json()
        assert result['first_name'] == user.profile.first_name

    async def test_forbidden_get_other_user_profile_for_user(
            self,
            moc_users,
            new_client,
            db_session
    ):
        """Тест запрета получения чужого профиля текущим юзером."""
        user: User = await _get_user(1, db_session)
        other_user: User = await _get_user(2, db_session)
        response: Response = await new_client.post(
           '/auth/jwt/login',
           data={'username': user.email, 'password': 'qwerty'},
        )
        access_token = response.json().get('access_token')
        new_client.headers.update({'Authorization': f'Bearer {access_token}'})
        response = await new_client.get(
            f'/profiles/{other_user.profile.id}'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_get_photo_from_self_profile(
            self,
            moc_users,
            db_session,
            new_client,
    ):
        """Тест получения фото своего профиля юзером."""
        user: User = await _get_user(1, db_session)
        response: Response = await new_client.post(
           '/auth/jwt/login',
           data={'username': user.email, 'password': 'qwerty'},
        )
        access_token = response.json().get('access_token')
        new_client.headers.update({'Authorization': f'Bearer {access_token}'})
        response = await new_client.get(
            '/profiles/me/photo'
        )
        assert response.status_code == status.HTTP_200_OK

    async def test_update_self_profile(
            self,
            moc_users,
            db_session,
            new_client: TestClient
    ):
        """Тест апдейта своего профиля."""
        user: User = await _get_user(1, db_session)
        response: Response = await new_client.post(
           '/auth/jwt/login',
           data={'username': user.email, 'password': 'qwerty'},
        )
        access_token = response.json().get('access_token')
        new_client.headers.update({'Authorization': f'Bearer {access_token}'})
        data = {'first_name': 'new_first_name'}
        response = await new_client.patch(
            '/profiles/me',
            json=data
        )
        assert response.status_code == status.HTTP_200_OK
        user: User = await _get_user(1, db_session)
        assert user.profile.first_name == 'new_first_name'

    async def test_update_photo(
            self,
            moc_users,
            db_session,
            new_client: TestClient
    ):
        """Тест апдейта фото своего профиля."""
        user: User = await _get_user(1, db_session)
        photo = user.profile.image
        tmp_image = Image.new('RGB', (640, 480))
        buffer = io.BytesIO()
        Path(
            settings.base_dir / 'tmp_for_load'
        ).mkdir(parents=True, exist_ok=True)
        tmp_image.save(settings.base_dir / 'tmp_for_load' / 'img.jpeg', 'jpeg')
        tmp_image.save(buffer, format='JPEG')
        img_str = base64.b64encode(buffer.getvalue())
        response: Response = await new_client.post(
           '/auth/jwt/login',
           data={'username': user.email, 'password': 'qwerty'},
        )
        access_token = response.json().get('access_token')
        new_client.headers.update({'Authorization': f'Bearer {access_token}'})
        with open(settings.base_dir / 'media' / photo, 'rb') as f:
            current_photo = base64.b64encode(f.read())
        response = await new_client.patch(
            '/profiles/me/update_photo',
            files={
                'file': (
                    'img.jpeg',
                    open(f'{settings.base_dir}/tmp_for_load/img.jpeg', 'rb'),
                    'image/jpeg'
                )
            }
        )
        user: User = await _get_user(1, db_session)
        with open(settings.base_dir / 'media' / user.profile.image, 'rb') as f:
            new_photo = base64.b64encode(f.read())
        assert new_photo == img_str
        assert current_photo != new_photo
        path = Path(f'{settings.base_dir}/media/{user.profile.image}')
        Path.unlink(path)
        delete_tmpdir(settings.base_dir / 'tmp_for_load')

    async def test_create_profile_deprecated(
            self,
            new_client: TestClient
    ):
        """Тест запрета создания профиля без создания юзера."""
        response = await new_client.post(
            '/profiles/',
            json={
                'first_name': 'test_first_name',
                'last_name': 'test_last_name',
                'age': 47
            }
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    async def test_forbidden_delete_profile(
            self,
            moc_users,
            db_session,
            auth_superuser: AsyncGenerator | TestClient
    ):
        """Тест запрета удаления профиля."""
        user = await _get_user(1, db_session)
        response = await auth_superuser.delete(
            f'/profiles/{user.profile.id}'
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
