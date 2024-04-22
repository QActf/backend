import enum

from fastapi_users.router.common import ErrorCode

from app.api_docs_responses.utils_docs import (
    LOGIN_WARNING, get_200_docs, get_204_docs, get_401_docs, get_403_docs,
    get_404_docs, get_405_docs
)


class RouteEnum(enum.IntEnum):
    auth_login = 0
    auth_logout = 1
    auth_register = 2
    get_users_me = 3
    patch_users_me = 4
    get_users_id = 5
    update_user_id = 6
    del_users_id = 7


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

USER_ME_SUMMARY = 'Получение информации о текущем ползователе.'
USER_ME_DESCRIPTION = """
    Получение информации о текущем зарегистрированным пользователем.

    Args:\n
        None.\n
    Returns:\n
        dict: Текущий пользователь.\n
    Permissions:\n
        Только зарегистрированный пользователь.\n
"""

USER_ME_PATCH_SUMMARY = 'Редактирование пользователя.'
USER_ME_PATCH_DESCRIPTION = """
    Изменение учетных данных пользователя.

    Args:\n
        None.\n
    Returns:\n
        dict: Текущий пользователь.\n
    Permissions:\n
        Только зарегистрированный пользователь по его id.\n
"""

USER_ID_SUMMARY = 'Информация пользователя по id.'
USER_ID_DESCRIPTION = """
    Получение информации о пользователе по его id.

    Args:\n
        int: id\n
    Returns:\n
        dict: Пользователь по id.\n
    Permissions:\n
        Только зарегистрированный пользователь.\n
"""

USER_ID_PATCH_SUMMARY = 'Редактирование пользователя по id.'
USER_ID_PATCH_DESCRIPTION = """
    Пользователь может изменить свои данные, которые ему достыпны для этого.

    Args:\n
        int: id\n
    Returns:\n
        dict: Текущий пользователь.\n
    Permissions:\n
        Только зарегистрированный пользователь c данным id.\n
"""

USER_ID_DEL_SUMMARY = 'Удаление пользователя по id.'
USER_ID_DEL_DESCRIPTION = """
    Удаление зарегистрированного пользователя по его id.

    Args:\n
        int: id пользователя, которого неоходимо удалить.\n
    Returns:\n
        None.\n
    Permissions:\n
        Только суперпользователь.\n
"""


def add_router_doc(router):
    router.routes[RouteEnum.auth_login].responses = LOGIN_USER
    router.routes[RouteEnum.auth_login].description = LOGIN_WARNING

    router.routes[RouteEnum.auth_logout].responses = LOGOUT_USER

    router.routes[RouteEnum.get_users_me].responses = GET_CURRENT_USER
    router.routes[RouteEnum.get_users_me].summary = USER_ME_SUMMARY
    router.routes[RouteEnum.get_users_me].description = USER_ME_DESCRIPTION

    router.routes[RouteEnum.patch_users_me].responses = UPDATE_CURRENT_USER
    router.routes[RouteEnum.patch_users_me].summary = USER_ME_PATCH_SUMMARY
    router.routes[
        RouteEnum.patch_users_me].description = USER_ME_PATCH_DESCRIPTION

    router.routes[RouteEnum.get_users_id].responses = GET_USER_BY_ID
    router.routes[RouteEnum.get_users_id].summary = USER_ID_SUMMARY
    router.routes[RouteEnum.get_users_id].description = USER_ID_DESCRIPTION

    router.routes[RouteEnum.update_user_id].responses = UPDATE_USER_BY_ID
    router.routes[RouteEnum.update_user_id].summary = USER_ID_PATCH_SUMMARY
    router.routes[
        RouteEnum.update_user_id].description = USER_ID_PATCH_DESCRIPTION

    router.routes[RouteEnum.del_users_id].summary = USER_ID_DEL_SUMMARY
    router.routes[RouteEnum.del_users_id].description = USER_ID_DEL_DESCRIPTION
