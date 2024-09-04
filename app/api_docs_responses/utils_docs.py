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
TASK_CREATE_VALUE = {
    'all_data': {
        'summary': 'Все обязательные поля задачи заполнены.',
        'value': {
            'name': 'Имя',
            'description': 'Описание',
            'difficult': 1
        }
    },
    'not_description_data': {
        'summary': 'Задача без указания описания.',
        'value': {'name': 'Имя', 'difficult': 1}
    },
    'not_difficult_data': {
        'summary': 'Задача без указания сложности.',
        'value': {'name': 'Имя', 'description': 'Описание'}
    },
    'empty_data': {
        'summary': 'Без данных.',
        'description': 'Validation Error 422',
        'value': {}
    }
}
TASK_UPDATE_VALUE = {
    'task_with_all_fields': {
        'summary': 'Обновить все поля задачи.',
        'value': {
            'difficult': 1,
            'name': 'Название задачи',
            'description': 'Описание задачи',
            'time': '8',
            'solvers': 8
        },
    },
    'tasks_new_name': {
        'summary': 'Обновить только название задачи.',
        'value': {'name': 'Новое название задачи'},
    },
    'tasks_new_description': {
        'summary': 'Обновить только описание задачи.',
        'value': {'description': 'Новое описание задачи'},
    },
    'tasks_new_difficult': {
        'summary': 'Обновить только сложность задачи.',
        'value': {'difficult': 8},
    },
    'tasks_new_time': {
        'summary': 'Обновить только среднее время решения задачи.',
        'value': {'time': '8'},
    },
    'tasks_new_solvers': {
        'summary': 'Обновить только количество пользователей решивших задачу.',
        'value': {'solvers': 8},
    }
}
PROFILE_UPDATE_VALUE = {
    'first_name': 'Имя',
    'last_name': 'Фамилия',
    'birthday': '1976-05-28',
    'gender': 'female',
}
USER_VALUE = {
    'password': 'Пароль',
    'email': 'user@example.com',
    'is_active': True,
    'is_superuser': True,
    'is_verified': True,
    'role': 'user',
    'username': 'Имя'
}
COURSE_VALUE = {
    'all_data': {
        'summary': 'Все поля заполнены.',
        'value': {
            'name': 'Новое название курса',
            'description': 'Новое описание курса',
        }
    },
    'only_name_data': {
        'summary': 'Только имя.',
        'value': {'name': 'Новое название курса'}
    },
    'only_description_data': {
        'summary': 'Только описание.',
        'value': {'description': 'Новое описание курса'}
    },
    'empty_data': {
        'summary': 'Без данных',
        'description': 'Validation Error 422',
        'value': {}
    }
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
