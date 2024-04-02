from fastapi_users.router.common import ErrorCode

from app.api_docs_responses.utils_docs import (get_200_dosc, get_204_dosc,
                                               get_401_dosc, get_405_dosc)

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

CREATE_AUTH = {
    **get_200_dosc(auth_context),
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
    **get_204_dosc(),
    **get_401_dosc()
}


DELETE_USER = {
    **get_204_dosc(),
    **get_405_dosc("Удаление пользователей запрещено!")
}
