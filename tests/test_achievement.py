from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Achievement, Profile, User

from .utils import get_obj_by_id, get_obj_count

CREATE_SCHEME = {
    'name': 'Achievment name',
    'description': 'Achievment description'
}
WRONG_CREATE_SCHEME = {
    'description': 'Achievment description'
}
UPDATE_SCHEME = {
    'name': 'new achievement name'
}


async def _get_achievement_by_id(
        index: int,
        db_session: AsyncSession
):
    """Возвращает ачивмент по id."""
    stmt = (
        select(Achievement)
        .where(Achievement.id == index)
        .options(
            selectinload(Achievement.profiles)
        )
    )
    achievement = await db_session.execute(stmt)
    return achievement.scalar()


async def _get_user_by_id(
        index: int,
        db_session: AsyncSession
):
    """Возвращает юзера по id."""
    user = await db_session.execute(
        select(User)
        .where(User.id == index)
        .options(
            selectinload(User.profile)
            .selectinload(Profile.achievements)
        )
    )
    return user.scalar()


async def _get_profile_by_user_id(
        index: int,
        db_session: AsyncSession
):
    """Возвращает профиль юзера."""
    profile = await db_session.execute(
        select(Profile)
        .where(Profile.user_id == index)
    )
    return profile.scalar()


class TestCreateAchievement:
    async def test_create_achievement_superuser(
            self,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест создания ачивмент."""
        achievements = await get_obj_count(Achievement, db_session)
        response = await auth_superuser.post(
            '/achievements/',
            json=CREATE_SCHEME
        )
        assert response.status_code == status.HTTP_201_CREATED
        new_achievements = await get_obj_count(Achievement, db_session)
        assert new_achievements == achievements + 1

    async def test_wrong_create_scheme(
            self,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест с неправильными данными для ачивмент."""
        achievements = await get_obj_count(Achievement, db_session)
        response = await auth_superuser.post(
            '/achievements/',
            json=WRONG_CREATE_SCHEME
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        new_achievements = await get_obj_count(Achievement, db_session)
        assert new_achievements == achievements

    async def test_forbidden_create_achievement_user(
            self,
            db_session: AsyncSession,
            auth_client: TestClient
    ):
        """Тест запрета создания ачивмент юзером."""
        achievements = await get_obj_count(Achievement, db_session)
        response = await auth_client.post(
            '/achievements/',
            json=CREATE_SCHEME
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        new_achievements = await get_obj_count(Achievement, db_session)
        assert new_achievements == achievements

    async def test_forbidden_create_achievement_nonauth(
            self,
            db_session: AsyncSession,
            new_client: TestClient
    ):
        """Тест запрета создания ачивмент юзером."""
        achievements = await get_obj_count(Achievement, db_session)
        response = await new_client.post(
            '/achievements/',
            json=CREATE_SCHEME
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        new_achievements = await get_obj_count(Achievement, db_session)
        assert new_achievements == achievements


class TestGetAchievement:
    async def test_get_all_achievements_superuser(
            self,
            moc_achievements,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест получения всех ачивмент суперюзером."""
        achievements = await get_obj_count(Achievement, db_session)
        response = await auth_superuser.get('/achievements/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == achievements

    async def test_forbidden_get_all_achievements_user(
            self,
            moc_achievements,
            db_session: AsyncSession,
            auth_client: TestClient
    ):
        """Тест запрета получения всех ачивмент юзером."""
        response = await auth_client.get('/achievements/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_forbidden_get_all_achievements_nonauth(
            self,
            moc_achievements,
            new_client: TestClient
    ):
        """Тест запрета получения ачивментс неавторизованным."""
        response = await new_client.get('/achievements/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_get_self_achievements_user(
            self,
            register_client,
            moc_users,
            moc_achievements,
            db_session: AsyncSession,
            auth_client: TestClient
    ):
        """Тест получения юзером своих ачивментс."""
        user = await _get_user_by_id(register_client.id, db_session)
        profile = await _get_profile_by_user_id(user.id, db_session)
        achievement = await _get_achievement_by_id(1, db_session)
        achiv = await _get_achievement_by_id(2, db_session)
        achiv.profiles.append(profile)
        achievement.profiles.append(profile)
        await db_session.commit()
        response = await auth_client.get('achievements/me')
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert len(result) == 2
        assert result[0]['id'] in (1, 2)
        assert result[1]['id'] in (1, 2)
        assert result[0]['id'] != result[1]['id']

    async def test_get_self_achievement_by_id_user(
            self,
            register_client,
            moc_users,
            moc_achievements,
            db_session: AsyncSession,
            auth_client: TestClient
    ):
        """Тест получения юзером своего ачивмент по id."""
        user = await _get_user_by_id(register_client.id, db_session)
        profile = await _get_profile_by_user_id(user.id, db_session)
        achievement = await _get_achievement_by_id(1, db_session)
        achiv = await _get_achievement_by_id(2, db_session)
        achiv.profiles.append(profile)
        achievement.profiles.append(profile)
        await db_session.commit()
        response = await auth_client.get('/achievements/me/1')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['id'] == 1
        response = await auth_client.get('/achievements/me/3')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        response = await auth_client.get('/achievements/me/22')
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateAchievement:
    async def test_forbidden_update_achievement_user(
            self,
            moc_achievements,
            db_session: AsyncSession,
            auth_client: TestClient
    ):
        """Тест запрета апдейта ачивмент юзером."""
        response = await auth_client.patch(
            '/achievements/1'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_forbidden_update_achievement_nonauth(
            self,
            moc_achievements,
            db_session: AsyncSession,
            new_client: TestClient
    ):
        """Тест запрета апдейта ачивмент неавторизованным."""
        response = await new_client.patch(
            '/achievements/1'
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_update_achievement_superuser(
            self,
            moc_achievements,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест апдейта ачивмент суперюзером."""
        achievement = await get_obj_by_id(1, Achievement, db_session)
        response = await auth_superuser.patch(
            '/achievements/1',
            json=UPDATE_SCHEME
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['name'] == UPDATE_SCHEME['name']
        check_achievement = await get_obj_by_id(1, Achievement, db_session)
        assert check_achievement.name == UPDATE_SCHEME['name']
        assert check_achievement.description == achievement.description


class TestDeleteAchievement:
    async def test_forbidden_delete_acievement_user(
            self,
            moc_achievements,
            db_session: AsyncSession,
            auth_client: TestClient
    ):
        """Тест запрета удаления ачивмент юзером."""
        achievements = await get_obj_count(Achievement, db_session)
        assert achievements > 0
        response = await auth_client.delete('/achievements/1')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        check_achiv = await get_obj_count(Achievement, db_session)
        assert check_achiv == achievements

    async def test_forbidden_delete_acievement_nonauth(
            self,
            moc_achievements,
            db_session: AsyncSession,
            new_client: TestClient
    ):
        """Тест запрета удаления ачивмент неавторизованным."""
        achievements = await get_obj_count(Achievement, db_session)
        assert achievements > 0
        response = await new_client.delete('/achievements/1')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        check_achiv = await get_obj_count(Achievement, db_session)
        assert check_achiv == achievements

    async def test_delete_achievement_superuser(
            self,
            moc_achievements,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест удаления ачивмент суперюзером."""
        achievement = await _get_achievement_by_id(1, db_session)
        assert achievement is not None
        achiv_count = await get_obj_count(Achievement, db_session)
        response = await auth_superuser.delete('/achievements/1')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        removed_achiv = await _get_achievement_by_id(1, db_session)
        assert removed_achiv is None
        check_achiv_count = await get_obj_count(Achievement, db_session)
        assert check_achiv_count == achiv_count - 1


class TestPaginationGroup:
    async def test_pagination(
            self,
            moc_achievements,
            auth_superuser: TestClient
    ):
        """Тест пагинации профилей."""
        response = await auth_superuser.get(
            '/achievements/?limit=2'
        )
        result = response.json()
        assert len(result) == 2
        assert result[0]['id'] == 1
        assert result[1]['id'] == 2
        response = await auth_superuser.get(
            '/achievements/?offset=2&limit=2'
        )
        result = response.json()
        assert len(result) == 2
        assert result[0]['id'] == 3
        assert result[1]['id'] == 4
