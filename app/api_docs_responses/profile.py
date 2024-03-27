GET_PROFILES = {
    200: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': [
                    {
                        "id": 0,
                        "first_name": 'Имя',
                        "last_name": 'Фамилия',
                        "age": 0,
                        "user_id": 0,
                        "image": 'Ссылка на изображение'
                    }
                ]
            }
        }
    },
    401: {
        'content': {
            'application/json': {
                "example": {"detail": "Unauthorized"}
            }
        }
    }
}

GET_PROFILE = {
    200: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': {
                    "id": 0,
                    "first_name": 'Имя',
                    "last_name": 'Фамилия',
                    "age": 0,
                    "user_id": 0,
                    "image": 'Ссылка на изображение'
                }
            }
        }
    },
    401: {
        'content': {
            'application/json': {
                "example": {"detail": "Unauthorized"}
            }
        }
    }
}
GET_PROFILE_PHOTO = {
    200: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': 'Ссылка на изображение'
            }
        }
    },
    401: {
        'content': {
            'application/json': {
                "example": {"detail": "Unauthorized"}
            }
        }
    }
}
CREATE_PROFILE = {
    200: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': {
                    "id": 0,
                    "first_name": 'Имя',
                    "last_name": 'Фамилия',
                    "age": 0,
                    "user_id": 0,
                    "image": 'Ссылка на изображение'
                }
            }
        }
    },
    405: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                "example": {
                    "detail": "Профиль создаётся автоматически при "
                    "создании пользователя. Используйте метод PATCH."
                }
            }
        }
    }
}
DELETE_PROFILE = {
    204: {
        'content': {
            'application/json': {
                'example': ""
            }
        }
    },
    405: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                "example": {
                    "detail": "Профиль удаляется при удалении пользователя."
                }
            }
        }
    }
}
