from typing import AsyncGenerator

import pytest_asyncio
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from httpx import AsyncClient
from passlib.hash import bcrypt

from app.core.db import get_async_session
from app.models.user import User

USER_EMAIL = 'testuser@example.com'
USER_PASSWORD = 'password'
USER_USERNAME = 'testuser'


@pytest_asyncio.fixture
async def new_client(
    prepare_database: FastAPI,
    db_session
) -> AsyncGenerator | TestClient:
    """Фикстура создания нового клиента."""
    async def _get_test_db():
        yield db_session
    prepare_database.dependency_overrides[get_async_session] = _get_test_db
    async with AsyncClient(
        app=prepare_database,
        base_url='http://testserver',
    ) as client:
        yield client


@pytest_asyncio.fixture
async def register_client(
    prepare_database: FastAPI,
    db_session
) -> AsyncGenerator:
    """Фикстура зарегистрированного клиента."""
    hashed_password = bcrypt.hash(USER_PASSWORD)
    register_user = User(
        email=USER_EMAIL,
        hashed_password=hashed_password,
        role='user',
        username=USER_USERNAME
    )
    db_session.add(register_user)
    await db_session.commit()
    await db_session.refresh(register_user)
    yield register_user


@pytest_asyncio.fixture
async def auth_client(
    new_client,
    register_client
) -> AsyncGenerator | TestClient:
    """Фикстура для клиента, вошедшего в систему."""
    response = await new_client.post(
        '/auth/jwt/login',
        data={'username': USER_EMAIL, 'password': USER_PASSWORD})
    assert response.status_code == status.HTTP_200_OK
    access_token = response.json().get('access_token')
    new_client.headers.update({'Authorization': f'Bearer {access_token}'})
    yield new_client


@pytest_asyncio.fixture
async def superuser(
    db_session
):
    """Фикстура суперюзера."""
    hashed_password = bcrypt.hash('admin')
    superuser = User(
        email='admin@admin.com',
        hashed_password=hashed_password,
        role='admin',
        username='admin',
        is_superuser=True
    )
    db_session.add(superuser)
    await db_session.commit()
    await db_session.refresh(superuser)
    yield superuser


@pytest_asyncio.fixture
async def auth_superuser(
    new_client: TestClient,
    superuser,
) -> AsyncGenerator | TestClient:
    """Фикстура для суперюзера, вошедшего в систему."""
    data = {
        'username': 'admin@admin.com',
        'password': 'admin'
    }
    response = await new_client.post(
        '/auth/jwt/login', data=data,
    )
    assert response.status_code == status.HTTP_200_OK
    access_token = response.json().get('access_token')
    new_client.headers.update({'Authorization': f'Bearer {access_token}'})
    yield new_client
