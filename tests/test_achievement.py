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
            moc_users,
            moc_achievements,
            register_client,
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
        profile = Profile(
            first_name='testuser_first_name',
            last_name='testuser_last_name',
            age=47,
            user_id=user.id
        )
        db_session.add(profile)
        await db_session.commit()
        await db_session.refresh(profile)
        # await db_session.refresh(user)
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
        await db_session.refresh(achievement)
        await db_session.refresh(user)
        print(achievement)
        print(user.id)
        user = await db_session.execute(
            select(User)
            .options(
                selectinload(User.profile)
                .selectinload(Profile.achievements)
            )
            .where(User.id == user.id)

        )
        user = user.scalars().first()
        response = auth_client.get('achievements/me')
        assert response.status_code == status.HTTP_200_OK
        print(response.json())
        print(achievement)
        print(profile)
        print(user.profile)
        print(user.profile.achievements)
