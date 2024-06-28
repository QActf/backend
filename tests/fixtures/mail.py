import pytest
from aiosmtpd.controller import Controller

from app.core.config import settings


@pytest.fixture
def mock_mail_server() -> None:
    """Фикстура тестового почтового сервера."""
    if settings.EMAIL_MOCK_SERVER:
        controller = Controller(handler=None, port=settings.EMAIL_PORT)
        controller.start()
        yield
        controller.stop()
