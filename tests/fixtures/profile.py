from typing import AsyncGenerator

import pytest_asyncio
from passlib.hash import bcrypt
from sqlalchemy import select

from app.models import User, Profile
from tests.conftest import AsyncSessionLocalTest


@pytest_asyncio.fixture
async def moc_users(
    db_session: AsyncSessionLocalTest
) -> AsyncGenerator:
    """Фикстура заполнения базы юзерами с профилями."""
    hashed_password = bcrypt.hash('qwerty')
    moc_users = [
        User(
            email=f'user_{i}@example.com',
            hashed_password=hashed_password,
            role='user',
            username=f'user_{i}'
        ) for i in range(1, 6)
    ]
    db_session.add_all(moc_users)
    await db_session.commit()
    moc_users = await db_session.execute(select(User))
    moc_users = moc_users.scalars().all()
    moc_profiles = [
        Profile(
            first_name=f'name_{user.username}',
            last_name=f'surname_{user.username}',
            age=i + 20,
            user_id=user.id
        ) for i, user in enumerate(moc_users)
    ]
    db_session.add_all(moc_profiles)
    await db_session.commit()


# @pytest_asyncio.fixture
# async def user_1(
#     prepare_database: FastAPI,
#     db_session: AsyncSessionLocalTest
# ) -> AsyncGenerator:
#     """Фикстура зарегистрированного клиента."""
#     hashed_password = bcrypt.hash('qwerty')
#     user_1 = User(
#         email='user_1@example.com',
#         hashed_password=hashed_password,
#         role='user',
#         username='user_1'
#     )
#     db_session.add(user_1)
#     await db_session.commit()
#     await db_session.refresh(user_1)
#     profile_1 = Profile(
#         first_name='user_1_fn',
#         last_name='user_1_ln',
#         age=25,
#         user_id=user_1.id
#     )
#     db_session.add(profile_1)
#     await db_session.commit()


# @pytest_asyncio.fixture
# async def user_2(
#     prepare_database: FastAPI,
#     db_session: AsyncSessionLocalTest
# ) -> AsyncGenerator:
#     """Фикстура зарегистрированного клиента."""
#     hashed_password = bcrypt.hash('qwerty')
#     user_2 = User(
#         email='user_2@example.com',
#         hashed_password=hashed_password,
#         role='user',
#         username='user_2'
#     )
#     db_session.add(user_2)
#     await db_session.commit()
#     await db_session.refresh(user_2)
#     profile_2 = Profile(
#         first_name='user_2_fn',
#         last_name='user_2_ln',
#         age=47,
#         user_id=user_2.id
#     )
#     db_session.add(profile_2)
#     await db_session.commit()
