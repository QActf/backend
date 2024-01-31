from pathlib import Path
from typing import AsyncGenerator

import pytest_asyncio
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.db import Base
from app.main import app

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
TEST_DB = BASE_DIR / 'test.db'
DATABASE_URL_TEST = f'sqlite+aiosqlite:///{str(TEST_DB)}'

pytest_plugins = [
    'tests.fixtures.user',
    'tests.fixtures.profile',
]

engine_test = create_async_engine(
    DATABASE_URL_TEST,
    poolclass=NullPool,
    connect_args={'check_same_thread': False},
)

AsyncSessionLocalTest = sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)


@pytest_asyncio.fixture
async def prepare_database() -> AsyncGenerator:
    """Фикстура для создания тестовой БД."""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield app
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(prepare_database: FastAPI) -> AsyncGenerator:
    """Фикстура для создания асинхронного сеанса тестовой базы данных."""
    connection = await engine_test.connect()
    transaction = await connection.begin()
    session = AsyncSessionLocalTest(bind=connection)
    yield session
    await session.close()
    await transaction.rollback()
    await connection.close()
