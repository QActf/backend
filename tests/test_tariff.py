from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from app.models import Tariff

CREATE_SCHEME = {
    'name': 'Test tariff',
    'description': 'Test tariff description'
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
            new_client: TestClient
    ):
        response = new_client.get('/tariffs')
        assert response.status_code == status.HTTP_200_OK

    async def test_get_tariffs_user(
            self,
            moc_tariffs,
            auth_client: TestClient
    ):
        response = auth_client.get('/tariffs')
        assert response.status_code == status.HTTP_200_OK

    async def test_get_tariffs_superuser(
            self,
            moc_tariffs,
            auth_superuser: TestClient
    ):
        response = auth_superuser.get('/tariffs')
        assert response.status_code == status.HTTP_200_OK


class TestUpdateTariff:
    ...


class TestDeleteTariff:
    ...
