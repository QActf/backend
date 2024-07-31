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
            common=Common(**CREATE_SCHEME['common']),
            header=Header(**CREATE_SCHEME['header']),
            auth=Auth(**CREATE_SCHEME['auth']),
            contacts=Contacts(**CREATE_SCHEME['contacts']),
            help=Help(**CREATE_SCHEME['help']),
            main=Main(**CREATE_SCHEME['main']),
            restore=Restore(**CREATE_SCHEME['restore']),
            subscription=Subscription(**CREATE_SCHEME['subscription']),
            profile_user=ProfileUser(**CREATE_SCHEME['profile_user']),
            secure=Secure(**CREATE_SCHEME['secure']),
            achievements=Achievements(**CREATE_SCHEME['achievements']),
            tasks=Tasks(**CREATE_SCHEME['tasks']),
            question_banner=QuestionBanner(**CREATE_SCHEME['question_banner']),
            errors=Errors(**CREATE_SCHEME['errors']),
            months=Months(**CREATE_SCHEME['months']),
        ) for language in LANGUAGES
    ]
    db_session.add_all(mock_locales)
    await db_session.commit()
