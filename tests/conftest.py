from typing import AsyncGenerator

import pytest_asyncio
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.core.db import Base
from app.main import app

DATABASE_URL_TEST = f'{settings.database_url}_test'


fixtures = 'tests.fixtures'

pytest_plugins = [
    f'{fixtures}.user',
    f'{fixtures}.profile',
    f'{fixtures}.group',
    f'{fixtures}.achievement',
    f'{fixtures}.tariff',
    f'{fixtures}.task',
    f'{fixtures}.course',
    f'{fixtures}.examination'
]

engine_test = create_async_engine(
    DATABASE_URL_TEST,
    poolclass=NullPool,
)

AsyncSessionLocalTest = async_sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)


@pytest_asyncio.fixture()
async def prepare_database() -> AsyncGenerator:
    """Фикстура для создания тестовой БД."""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield app
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def db_session(prepare_database: FastAPI) -> AsyncGenerator:
    """Фикстура для создания асинхронного сеанса тестовой базы данных."""
    connection = await engine_test.connect()
    transaction = await connection.get_raw_connection()
    session = AsyncSessionLocalTest(bind=connection)
    yield session
    await session.close()
    transaction.rollback()
    await connection.close()
