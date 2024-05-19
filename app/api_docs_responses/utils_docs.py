'''Переменные и функции которые влияют только на отображение документации
 и не влияют на работу программы.
'''

LOGIN_WARNING = ('При отправки запроса необходимо в поле **username** '
                 'вводить **email** пользоватля.')
REQUEST_NAME_AND_DESCRIPTION_VALUE = {
    'all_data': {
        'summary': 'Все поля заполнены.',
        'value': {
            'name': 'Имя',
            'description': 'Описание'
        }
    },
    'not_all_data': {
        'summary': 'Только имя, без описания.',
        'value': {'name': 'Имя'}
    },
    'empty_data': {
        'summary': 'Без данных',
        'description': 'Validation Error 422',
        'value': {}
    }
}
PROFILE_UPDATE_VALUE = {'first_name': 'Имя', 'last_name': 'Фамилия', 'age': 20}
USER_VALUE = {
    'password': 'Пароль',
    'email': 'user@example.com',
    'is_active': True,
    'is_superuser': True,
    'is_verified': True,
    'role': 'user',
    'username': 'Имя'
}


def get_200_docs(content):
    return {
        200: {
            'description': 'Successful Response',
            'content': content
        }
    }


def get_201_docs(content):
    return {
        201: {
            'description': 'Created',
            'content': content
        }
    }


def get_204_docs():
    return {
        204: {
            'description': 'Запись удалена.',
            'content': {
                'application/json': {
                    'example': ''
                }
            }
        }
    }


def get_400_docs(detail):
    return {
        400: {
            'content': {
                'application/json': {
                    'example': {'detail': detail}
                }
            }
        }
    }


def get_401_docs(description=None):
    return {
        401: {
            'description': description,
            'content': {
                'application/json': {
                    'example': {'detail': 'Unauthorized'}
                }
            }
        }
    }


def get_403_docs(detail, description=None):
    return {
        403: {
            'description': description,
            'content': {
                'application/json': {
                    'example': {'detail': detail}
                }
            }
        }
    }


def get_404_docs(detail, description=None):
    return {
        404: {
            'description': description,
            'content': {
                'application/json': {
                    'example': {'detail': detail}
                }
            }
        }
    }


def get_405_docs(detail):
    return {
        405: {
            'description': 'Использование этого метода запрещено.',
            'content': {
                'application/json': {
                    'example': {
                        'detail': detail
                    }
                }
            }
        }
    }
