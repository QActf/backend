from fastapi_users.router.common import ErrorCode

from app.api_docs_responses.utils_docs import (
    get_200_docs, get_204_docs, get_401_docs, get_403_docs, get_404_docs,
    get_405_docs
)

auth_context = {
    'application/json': {
        'example': {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
            "eyJ1c2VyX2lkIjoiOTIyMWZmYzktNjQwZi00MzcyLTg2ZDMtY2U2NDJjYmE1NjA"
            "zIiwiYXVkIjoiZmFzdGFwaS11c2VyczphdXRoIiwiZXhwIjoxNTcxNTA0MTkzfQ."
            "M10bjOe45I5Ncu_uXvOmVV8QxnL-nZfcH96U90JaocI",
            "token_type": "bearer"
        }
    }
}

user_context = {
    'application/json': {
        'example': {
            "id": 0,
            "email": "user@example.com",
            "is_active": True,
            "is_superuser": False,
            "is_verified": True,
            "role": "user",
            "username": "Имя",
            "tariff_id": 0
        }
    }
}

status_400_for_update_user = {
    400: {
        'content': {
            "application/json": {
                "examples": {
                    ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS: {
                        "summary": (
                            "Пользователь с таким email уже существует."
                        ),
                        "value": {
                            "detail": (
                                ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS
                            )
                        },
                    },
                    ErrorCode.UPDATE_USER_INVALID_PASSWORD: {
                        "summary": "Вы не можете создать такой пароль.",
                        "value": {
                            "code": "UPDATE_USER_INVALID_PASSWORD",
                            "reason": "Password should beat least 3 characters"
                        },
                    },
                }
            }
        }
    }
}

LOGIN_USER = {
    **get_200_docs(auth_context),
    400: {
        'content': {
            "application/json": {
                "examples": {
                    ErrorCode.LOGIN_BAD_CREDENTIALS: {
                        "summary": "Неверные введённые данные или "
                        "пользователь не активет.",
                        "value": {
                            "detail": ErrorCode.LOGIN_BAD_CREDENTIALS
                        },
                    },
                    ErrorCode.LOGIN_USER_NOT_VERIFIED: {
                        "summary": "Пользоваетль не верифицирован.",
                        "value": {
                            "detail": ErrorCode.LOGIN_USER_NOT_VERIFIED
                        },
                    },
                }
            }
        }
    }
}

LOGOUT_USER = {
    **get_204_docs(),
    **get_401_docs()
}

GET_CURRENT_USER = {
    **get_200_docs(user_context),
    **get_401_docs()
}

GET_USER_BY_ID = {
    **get_200_docs(user_context),
    **get_401_docs('Отсутствует токен или неактивный пользователь.'),
    **get_403_docs('Forbidden', 'Нужны права superuser.'),
    **get_404_docs('Not found', 'Пользователь не найден.')
}
UPDATE_USER_BY_ID = {
    **get_200_docs(user_context),
    **status_400_for_update_user,
    **get_401_docs('Отсутствует токен или неактивный пользователь.'),
    **get_403_docs('Forbidden', 'Нужны права superuser.'),
    **get_404_docs('Not found', 'Пользователь не найден.')
}

UPDATE_CURRENT_USER = {
    **get_200_docs(user_context),
    **status_400_for_update_user,
    **get_401_docs()
}

DELETE_USER = {
    **get_204_docs(),
    **get_405_docs("Удаление пользователей запрещено!")
}
