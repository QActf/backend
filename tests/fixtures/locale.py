import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    Auth, Common, Contacts, Errors, Header, Help, Locale, Main, Restore,
    Subscription, Tasks,
)
from tests.test_locale import CREATE_SCHEME

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
            tasks=Tasks(**CREATE_SCHEME['tasks']),
            errors=Errors(**CREATE_SCHEME['errors']),
        ) for language in LANGUAGES
    ]
    db_session.add_all(mock_locales)
    await db_session.commit()
