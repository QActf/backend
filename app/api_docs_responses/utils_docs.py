'''Переменные и функции которые влияют только на отображение документации
 и не влияют на работу программы.
'''

LOGIN_WARNING = ('При отправки запроса необходимо в поле **username** '
                 'вводить **email** пользоватля.')
NAME_AND_DESCRIPTION_VALUE = {"name": "Название", "description": "Описание"}
PROFILE_UPDATE_VALUE = {"first_name": "Имя", "last_name": "Фамилия", "age": 20}
USER_VALUE = {
    "password": "Пароль",
    "email": "user@example.com",
    "is_active": True,
    "is_superuser": True,
    "is_verified": True,
    "role": "user",
    "username": "Имя"
}


def get_200_dosc(content):
    return {
        200: {
            'description': 'Successful Response',
            'content': content
        }
    }


def get_201_dosc(content):
    return {
        201: {
            'description': 'Created',
            'content': content
        }
    }


def get_204_dosc():
    return {
        204: {
            'description': 'Запись удалена.',
            'content': {
                'application/json': {
                    'example': ""
                }
            }
        }
    }


def get_400_dosc(detail):
    return {
        400: {
            'content': {
                'application/json': {
                    "example": {"detail": detail}
                }
            }
        }
    }


def get_401_dosc(description=None):
    return {
        401: {
            'description': description,
            'content': {
                'application/json': {
                    "example": {"detail": "Unauthorized"}
                }
            }
        }
    }


def get_403_dosc(detail, description=None):
    return {
        403: {
            'description': description,
            'content': {
                'application/json': {
                    "example": {"detail": detail}
                }
            }
        }
    }


def get_404_dosc(detail, description=None):
    return {
        404: {
            'description': description,
            'content': {
                'application/json': {
                    "example": {"detail": detail}
                }
            }
        }
    }


def get_405_dosc(detail):
    return {
        405: {
            'description': 'Использование этого метода запрещено.',
            'content': {
                'application/json': {
                    "example": {
                        "detail": detail
                    }
                }
            }
        }
    }
