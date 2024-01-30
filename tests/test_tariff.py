from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.models import Tariff

CREATE_SCHEME = {
    'name': 'Test tariff',
    'description': 'Test tariff description'
}
UPDATE_SCHEME = {
    'name': 'New tariff name'
}


class TestCreateTariff:
    async def test_forbidden_create_tarif_nonauth(
            self,
            new_client: TestClient
    ):
        response = new_client.post(
            '/tariffs'
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_forbidden_create_tarif_user(
            self,
            auth_client: TestClient
    ):
        response = auth_client.post(
            '/tariffs'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_create_tariff_superuser(
            self,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        stmt = func.count(Tariff.id)
        tariffs = await db_session.execute(stmt)
        tariffs = tariffs.scalar()
        response = auth_superuser.post(
            '/tariffs',
            json=CREATE_SCHEME
        )
        assert response.status_code == status.HTTP_201_CREATED
        check_tariffs = await db_session.execute(stmt)
        check_tariffs = check_tariffs.scalar()
        assert check_tariffs == tariffs + 1


class TestGetTariff:
    async def test_get_tariffs_nonauth(
            self,
            moc_tariffs,
            db_session: AsyncSession,
            new_client: TestClient
    ):
        """Тест получения всех тарифов."""
        stmt = func.count(Tariff.id)
        tariffs_count = await db_session.execute(stmt)
        tariffs_count = tariffs_count.scalar()
        response = new_client.get('/tariffs')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == tariffs_count

    async def test_get_tariff_by_id(
            self,
            moc_tariffs,
            db_session: AsyncSession,
            new_client: TestClient
    ):
        """Тест полученя тарифа по id."""
        stmt = select(Tariff).where(Tariff.id == 1)
        tariff = await db_session.execute(stmt)
        tariff = tariff.scalar()
        response = new_client.get('/tariffs/1')
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result['id'] == tariff.id


class TestUpdateTariff:
    async def test_forbidden_update_tariff_nonauth(
            self,
            moc_tariffs,
            new_client: TestClient
    ):
        """Тест запрета апдейта тарифа неавторизованным."""
        response = new_client.patch(
            '/tariffs/1'
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_forbidden_update_tariff_user(
            self,
            moc_tariffs,
            auth_client: TestClient
    ):
        """Тест запрета апдейта тарифа юзером."""
        response = auth_client.patch(
            '/tariffs/1'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_update_tariff(
            self,
            moc_tariffs,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест апдейта тарифа."""
        stmt = select(Tariff).where(Tariff.id == 1)
        tariff = await db_session.execute(stmt)
        tariff = tariff.scalar()
        response = auth_superuser.patch(
            '/tariffs/1',
            json=UPDATE_SCHEME
        )
        assert response.status_code == status.HTTP_200_OK
        check_tariff = await db_session.execute(stmt)
        check_tariff = check_tariff.scalar()
        assert check_tariff.name == UPDATE_SCHEME['name']
        assert check_tariff.description == tariff.description


class TestDeleteTariff:
    async def test_forbidden_delete_tariff_nonauth(
            self,
            moc_tariffs,
            new_client: TestClient
    ):
        """Тест запрета удаления тарифа неавторизованным."""
        response = new_client.delete('/tariffs/1')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_forbidden_delete_tariff_user(
            self,
            moc_tariffs,
            auth_client: TestClient
    ):
        """Тест запрета удаления тарифа юзером."""
        response = auth_client.delete('/tariffs/1')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_delete_tariff_superuser(
            self,
            moc_tariffs,
            db_session: AsyncSession,
            auth_superuser: TestClient
    ):
        """Тест удаления тарифа."""
        stmt_count = func.count(Tariff.id)
        tariff_count = await db_session.execute(stmt_count)
        tariff_count = tariff_count.scalar()
        stmt_tariff = select(Tariff).where(Tariff.id == 1)
        tariff = await db_session.execute(stmt_tariff)
        tariff = tariff.scalar()
        response = auth_superuser.delete('/tariffs/1')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        check_tariff_count = await db_session.execute(stmt_count)
        check_tariff_count = check_tariff_count.scalar()
        assert check_tariff_count == tariff_count - 1
        check_tariff = await db_session.execute(stmt_tariff)
        check_tariff = check_tariff.scalar()
        assert check_tariff is None
