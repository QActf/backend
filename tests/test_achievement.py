from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from app.models import Achievement

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

    async def test_forbidden_create_achievemrnt_user(
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

    async def test_forbidden_create_achievemrnt_nonauth(
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
