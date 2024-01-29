from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from app.models import Achievement

CREATE_SCHEME = {
    'name': 'Achievment name',
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
