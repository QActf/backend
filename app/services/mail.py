import logging
import re
from email.message import EmailMessage

from aiosmtpd.controller import Controller
from aiosmtplib import SMTP, errors

from app.core.config import settings

logger = logging.getLogger(__name__)


class MockEmailServer:
    def __init__(self, port=settings.EMAIL_PORT):
        self.port = port
        self.controller = Controller(handler=None, port=self.port)

    def start(self):
        """Запустит почтовый сервер."""
        self.controller.start()
        logger.info('Email server started on port %s.', self.port)


class MailMessage:
    def __init__(self, to=None, subject='', text=''):
        self.__from_email = settings.EMAIL_FROM
        self.to = to
        self.subject = subject
        self.text = text

    def _is_valid_to(self, to):
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,62}$'
        return re.match(regex, to)

    def _is_valid_subject(self, subject):
        if len(subject) > 3:
            return subject

    def __setattr__(self, key, value):
        if key == 'subject' and not self._is_valid_subject(value):
            raise ValueError('Subject must be more than 3 characters.')
        if key == 'to' and not self._is_valid_to(value):
            raise ValueError('It\'s not an email address.')
        super().__setattr__(key, value)

    async def send_email_message(self):
        message = EmailMessage()
        message['From'] = self.__from_email
        message['To'] = self.to
        message['Subject'] = self.subject
        message.set_content(self.text)

        if settings.EMAIL_MOCK_SERVER:
            smtp_client = SMTP(port=settings.EMAIL_PORT)
        else:
            smtp_client = SMTP(
                hostname=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_tls=settings.EMAIL_USE_TLS,
            )
        try:
            async with smtp_client:
                await smtp_client.send_message(message)
        except errors.SMTPConnectError as e:
            logger.exception('Нет соединения с SMTP сервером. %s', e)
        except errors.SMTPAuthenticationError as e:
            logger.exception('Ошибка соединения с SMTP сервером. %s', e)
        except Exception as e:
            logger.exception(
                'Во время отправки email что-то пошло не так: %s', e
            )
