from typing import AsyncGenerator

import pytest_asyncio
from passlib.hash import bcrypt
from sqlalchemy import select

from app.models import Profile, User


@pytest_asyncio.fixture
async def moc_users(
    db_session
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
