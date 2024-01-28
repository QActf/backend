from fastapi.testclient import TestClient
from sqlalchemy import select, Result, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Group

GROUP_SCHEME = {
    'name': 'Test Group',
    'description': 'Test Group Description'
}


class TestGroup:
    async def test_create_group(
            self,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Создание группы суперюзером"""
        stmt = func.count(Group.id)
        groups = await db_session.execute(stmt)
        groups = groups.scalar()
        response = auth_superuser.post(
            '/groups',
            json=GROUP_SCHEME
        )
        assert response.status_code == 201
        new_groups = await db_session.execute(stmt)
        new_groups = new_groups.scalar()
        assert new_groups == groups + 1

    async def test_forbidden_create_group_by_user(
            self,
            auth_client: TestClient
    ):
        """Тест запрета создания группы юзером"""
        response = auth_client.post(
            '/groups',
            json=GROUP_SCHEME
        )
        assert response.status_code == 403
