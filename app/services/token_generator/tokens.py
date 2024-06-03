import datetime

from app.core.config import settings

from .base_converter import base36_to_int, int_to_base36
from .crypto import constant_time_compare, salted_hmac


class TokenGenerator:
    """
    Генераци токена на основе HMAC.
    """
    key_salt = ''
    algorithm = None
    _secret = None

    def __init__(self):
        self.algorithm = self.algorithm or 'sha256'

    def _get_secret(self):
        return self._secret or settings.secret

    def _set_secret(self, secret):
        self._secret = secret

    @property
    def secret(self):
        return (self._get_secret, self._set_secret)

    @property
    def _now(self):
        return datetime.datetime.now()

    def make_token(self, user):
        """
        Возвращает токен который можно использовать единажды
        для конкретного пользователя.
        """
        return self._make_token_with_timestamp(
            user,
            self._num_seconds(self._now)
        )

    def _make_token_with_timestamp(self, user, timestamp):
        timestamp_b36 = int_to_base36(timestamp)
        hash_string = salted_hmac(
            self.key_salt,
            self._make_hash_value(user, timestamp),
            secret=self.secret,
            algorithm=self.algorithm,
        ).hexdigest()[::2]  # Limit to shorten the URL.
        return f'{timestamp_b36}-{hash_string}'

    def _make_hash_value(self, user, timestamp):
        # login_timestamp = '' if user.last_login is None
        # else user.last_login.replace(microsecond=0, tzinfo=None)
        login_timestamp = ''
        # email_field = user.get_email_field_name()
        email = getattr(user, 'email', '') or ''
        return (
            f'{user.id}{user.hashed_password}'
            f'{login_timestamp}{timestamp}{email}'
        )

    def _num_seconds(self, dt):
        return int((dt - datetime.datetime(2001, 1, 1)).total_seconds())

    def check_token(self, user, token):
        """
        Check that a password reset token is correct for a given user.
        """
        if not (user and token):
            return False
        # Parse the token
        try:
            ts_b36, _ = token.split('-')
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(
            self._make_token_with_timestamp(user, ts),
            token,
        ):
            return False

        # Check the timestamp is within limit.
        if (self._num_seconds(self._now) - ts) > 5000:
            # settings.PASSWORD_RESET_TIMEOUT:
            return False

        return True


token_generator = TokenGenerator()
