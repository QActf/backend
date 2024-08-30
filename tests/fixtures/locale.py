import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    Achievements, Auth, Common, Contacts, Errors, Header, Help, Locale, Main,
    Months, ProfileUser, QuestionBanner, Restore, Secure, Subscription, Tasks,
)
from tests.test_locale import CREATE_SCHEMA

LANGUAGES = ('en', 'ru', 'ch')


@pytest_asyncio.fixture
async def mock_locales(db_session: AsyncSession) -> None:
    """Фикстура создания набора локалей."""
    mock_locales = [
        Locale(
            language=language,
            common=Common(**CREATE_SCHEMA['common']),
            header=Header(**CREATE_SCHEMA['header']),
            auth=Auth(**CREATE_SCHEMA['auth']),
            contacts=Contacts(**CREATE_SCHEMA['contacts']),
            help=Help(**CREATE_SCHEMA['help']),
            main=Main(**CREATE_SCHEMA['main']),
            restore=Restore(**CREATE_SCHEMA['restore']),
            subscription=Subscription(**CREATE_SCHEMA['subscription']),
            profile_user=ProfileUser(**CREATE_SCHEMA['profile_user']),
            secure=Secure(**CREATE_SCHEMA['secure']),
            achievements=Achievements(**CREATE_SCHEMA['achievements']),
            tasks=Tasks(**CREATE_SCHEMA['tasks']),
            question_banner=QuestionBanner(**CREATE_SCHEMA['question_banner']),
            errors=Errors(**CREATE_SCHEMA['errors']),
            months=Months(**CREATE_SCHEMA['months']),
        ) for language in LANGUAGES
    ]
    db_session.add_all(mock_locales)
    await db_session.commit()
