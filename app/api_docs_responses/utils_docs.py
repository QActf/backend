'''Переменные и функции которые влияют только на отображение документации
 и не влияют на работу программы.
'''


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


def get_204_dosc():
    return {
        204: {
            'descripton': 'Success',
            'content': {
                'application/json': {
                    'example': ""
                }
            }
        }
    }


def get_401_dosc():
    return {
        401: {
            'content': {
                'application/json': {
                    "example": {"detail": "Unauthorized"}
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


def get_403_dosc(detail):
    return {
        403: {
            'content': {
                'application/json': {
                    "example": {"detail": detail}
                }
            }
        }
    }


def get_404_dosc(detail):
    return {
        404: {
            'content': {
                'application/json': {
                    "example": {"detail": detail}
                }
            }
        }
    }
