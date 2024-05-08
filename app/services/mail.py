import re
from email.message import EmailMessage
from http import HTTPStatus

from aiosmtplib import SMTP, errors
from fastapi import HTTPException

from app.core.config import settings


class MailMessage:
    def __init__(self, to=None, subject='', text=''):
        self.__from_email = settings.EMAIL_FROM
        self.to = to
        self.subject = subject
        self.text = text

    def _is_valid_to(self, to):
        regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,62}$"
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

        smtp_client = SMTP(
            hostname=settings.hostname,
            port=settings.port,
            username=settings.email_user,
            password=settings.password,
            use_tls=settings.use_tls,
        )
        try:
            async with smtp_client:
                await smtp_client.send_message(message)
        except errors.SMTPConnectError:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Нет соединения с SMTP сервером.',
            )
        except errors.SMTPAuthenticationError:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Ошибка соединения с SMTP сервером.',
            )
        except Exception:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='увы, что-то пошло не так.',
            )


hello_mail = MailMessage(
    subject='Welcome to QActf.',
    to='wildmv@gmail.com',
    text='Hello dear. we are warm welcome you to our web app.'
)
