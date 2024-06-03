import datetime
import hashlib
import hmac
import secrets

from app.core.config import settings

from .exceptions import InvalidAlgorithm

_PROTECTED_TYPES = (
    type(None), int, float, datetime.datetime, datetime.date, datetime.time,
)


def force_bytes(
    string,
    encoding='utf-8',
    strings_only=False,
    errors='strict'
):
    if isinstance(string, bytes):
        if encoding == 'utf-8':
            return string
        else:
            return string.decode('utf-8', errors).encode(encoding, errors)
    if strings_only and isinstance(string, _PROTECTED_TYPES):
        return string
    if isinstance(string, memoryview):
        return bytes(string)
    return str(string).encode(encoding, errors)


def constant_time_compare(value1, value2):
    return secrets.compare_digest(force_bytes(value1), force_bytes(value2))


def salted_hmac(key_salt, value, secret=None, *, algorithm='sha1'):
    """
    Возвращает обьект HMAC для числа value используя сгенерированный ключ
    Используется алгоритм SHA1б но доступны и другие.
    Для каждого использования HMAC должен быть передан разный key_salt. Но...
    """
    if secret is None:
        secret = settings.secret

    key_salt = force_bytes(key_salt)
    secret = force_bytes(secret)
    try:
        hasher = getattr(hashlib, algorithm)
    except AttributeError as e:
        raise InvalidAlgorithm(
            '%r не поддерживается модулем hashlib.'
            % algorithm
        ) from e
    key = hasher(key_salt + secret).digest()
    return hmac.new(key, msg=force_bytes(value), digestmod=hasher)


def encode_uid(id):
    return id


def decode_uid(id):
    return id
