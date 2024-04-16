from fastapi_users.router.common import ErrorCode

from app.api_docs_responses.utils_docs import get_201_docs

CREATE_REGISTER = {
    **get_201_docs({
        'application/json': {
            'example': {
                "id": 0,
                "email": "user@example.com",
                "is_active": True,
                "is_superuser": True,
                "is_verified": False,
                "role": "user",
                "username": "Имя",
                "tariff_id": 0
            }
        }
    }),
    400: {
        'content': {
            "application/json": {
                "examples": {
                    ErrorCode.REGISTER_USER_ALREADY_EXISTS: {
                        "summary": "Пользователь с таким email "
                        "уже существует.",
                        "value": {
                            "detail": ErrorCode.REGISTER_USER_ALREADY_EXISTS
                        },
                    },
                    ErrorCode.REGISTER_INVALID_PASSWORD: {
                        "summary": "Ошибка валидации пароля.",
                        "value": {
                            "detail": {
                                "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                                "reason": "Password should be"
                                "at least 3 characters",
                            }
                        },
                    },
                }
            }
        }
    }
}
