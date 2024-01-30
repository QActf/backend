from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.models import Achievement, User, Profile

CREATE_SCHEME = {
    'name': 'Achievment name',
    'description': 'Achievment description'
}
WRONG_CREATE_SCHEME = {
    'description': 'Achievment description'
}


class TestCreateAchievement:
    async def test_create_achievement_superuser(
            self,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест создания ачивмент."""
        stmt = func.count(Achievement.id)
        achievements = await db_session.execute(stmt)
        achievements = achievements.scalar()
        response = auth_superuser.post(
            '/achievements',
            json=CREATE_SCHEME
        )
        assert response.status_code == status.HTTP_201_CREATED
        new_achievements = await db_session.execute(stmt)
        new_achievements = new_achievements.scalar()
        assert new_achievements == achievements + 1

    async def test_wrong_create_scheme(
            self,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        stmt = func.count(Achievement.id)
        achievements = await db_session.execute(stmt)
        achievements = achievements.scalar()
        response = auth_superuser.post(
            '/achievements',
            json=WRONG_CREATE_SCHEME
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        new_achievements = await db_session.execute(stmt)
        new_achievements = new_achievements.scalar()
        assert new_achievements == achievements

    async def test_forbidden_create_achievement_user(
            self,
            db_session: AsyncSession,
            auth_client: TestClient
    ):
        """Тест запрета создания ачивмент юзером."""
        stmt = func.count(Achievement.id)
        achievements = await db_session.execute(stmt)
        achievements = achievements.scalar()
        response = auth_client.post(
            '/achievements',
            json=CREATE_SCHEME
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        new_achievements = await db_session.execute(stmt)
        new_achievements = new_achievements.scalar()
        assert new_achievements == achievements

    async def test_forbidden_create_achievement_nonauth(
            self,
            db_session: AsyncSession,
            new_client: TestClient
    ):
        """Тест запрета создания ачивмент юзером."""
        stmt = func.count(Achievement.id)
        achievements = await db_session.execute(stmt)
        achievements = achievements.scalar()
        response = new_client.post(
            '/achievements',
            json=CREATE_SCHEME
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        new_achievements = await db_session.execute(stmt)
        new_achievements = new_achievements.scalar()
        assert new_achievements == achievements


class TestGetAchievement:
    async def test_get_all_achievements_superuser(
            self,
            moc_achievements,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест получения всех ачивмент суперюзером."""
        stmt = func.count(Achievement.id)
        achievements = await db_session.execute(stmt)
        achievements = achievements.scalar()
        response = auth_superuser.get('/achievements')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == achievements

    async def test_forbidden_get_all_achievements_user(
            self,
            moc_achievements,
            db_session: AsyncSession,
            auth_client: TestClient
    ):
        """Тест запрета получения всех ачивмент юзером."""
        response = auth_client.get('/achievements')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_forbidden_get_all_achievements_nonauth(
            self,
            moc_achievements,
            new_client: TestClient
    ):
        """Тест запрета получения ачивментс неавторизованным."""
        response = new_client.get('/achievements')
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
        user = await db_session.execute(
            select(User)
            .where(User.username == register_client.username)
            .options(
                selectinload(User.profile)
                .selectinload(Profile.achievements)
            )
        )
        user = user.scalars().first()
        profile = await db_session.execute(
            select(Profile)
            .where(Profile.user_id == user.id)
        )
        profile = profile.scalars().first()
        achievement = await db_session.execute(
            select(Achievement)
            .where(Achievement.id == 1)
            .options(
                selectinload(Achievement.profiles)
            )
        )
        achievement = achievement.scalars().first()
        achiv = await db_session.execute(
            select(Achievement)
            .where(Achievement.id == 2)
            .options(
                selectinload(Achievement.profiles)
            )
        )
        achiv = achiv.scalars().first()
        achiv.profiles.append(profile)
        achievement.profiles.append(profile)
        await db_session.commit()
        response = auth_client.get('achievements/me')
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
        user = await db_session.execute(
            select(User)
            .where(User.username == register_client.username)
            .options(
                selectinload(User.profile)
                .selectinload(Profile.achievements)
            )
        )
        user = user.scalars().first()
        profile = await db_session.execute(
            select(Profile)
            .where(Profile.user_id == user.id)
        )
        profile = profile.scalars().first()
        achievement = await db_session.execute(
            select(Achievement)
            .where(Achievement.id == 1)
            .options(
                selectinload(Achievement.profiles)
            )
        )
        achievement = achievement.scalars().first()
        achiv = await db_session.execute(
            select(Achievement)
            .where(Achievement.id == 2)
            .options(
                selectinload(Achievement.profiles)
            )
        )
        achiv = achiv.scalars().first()
        achiv.profiles.append(profile)
        achievement.profiles.append(profile)
        await db_session.commit()
        response = auth_client.get('/achievements/me/1')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['id'] == 1
        response = auth_client.get('/achievements/me/3')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        response = auth_client.get('/achievements/me/22')
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateAchievement:
    ...


class TestDeleteAchievement:
    async def test_forbidden_delete_acievement_user(
            self,
            moc_achievements,
            db_session: AsyncSession,
            auth_client: TestClient
    ):
        """Тест запрета удаления ачивмент юзером."""
        achievements = await db_session.execute(
            func.count(Achievement.id)
        )
        achievements = achievements.scalar()
        assert achievements > 0
        response = auth_client.delete('/achievements/1')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        check_achiv = await db_session.execute(
            func.count(Achievement.id)
        )
        check_achiv = check_achiv.scalar()
        assert check_achiv == achievements

    async def test_forbidden_delete_acievement_nonauth(
            self,
            moc_achievements,
            db_session: AsyncSession,
            new_client: TestClient
    ):
        """Тест запрета удаления ачивмент неавторизованным."""
        achievements = await db_session.execute(
            func.count(Achievement.id)
        )
        achievements = achievements.scalar()
        assert achievements > 0
        response = new_client.delete('/achievements/1')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        check_achiv = await db_session.execute(
            func.count(Achievement.id)
        )
        check_achiv = check_achiv.scalar()
        assert check_achiv == achievements

    async def test_delete_achievement_superuser(
            self,
            moc_achievements,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест удаления ачивмент суперюзером."""
        achievement = await db_session.execute(
            select(Achievement)
            .where(Achievement.id == 1)
        )
        achievement = achievement.scalar()
        achiv_count = await db_session.execute(
            func.count(Achievement.id)
        )
        achiv_count = achiv_count.scalar()
        response = auth_superuser.delete('/achievements/1')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        removed_achiv = await db_session.execute(
            select(Achievement)
            .where(Achievement.id == 1)
        )
        removed_achiv = removed_achiv.scalar()
        assert removed_achiv is None
        check_achiv_count = await db_session.execute(
            func.count(Achievement.id)
        )
        check_achiv_count = check_achiv_count.scalar()
        assert check_achiv_count == achiv_count - 1
