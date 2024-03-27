GET_COURSES = {
    200: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': [
                    {
                        'id': 0,
                        'name': 'Название курса',
                        'description': 'Описание курса'
                    }
                ]
            }
        }
    }
}
GET_USER_COURSES = {
    200: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': [
                    {
                        'id': 0,
                        'name': 'Название курса',
                        'description': 'Описание курса'
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
GET_USER_COURSE = {
    200: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': [
                    {
                        'id': 0,
                        'name': 'Название курса',
                        'description': 'Описание курса'
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
    },
    403: {
        'content': {
            'application/json': {
                "example": {"detail": "Вы не записаны на данный курс."}
            }
        }
    }
}

GET_COURSE = {
    200: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': {
                    'id': 0,
                    'name': 'Название курса',
                    'description': 'Описание курса'
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

CREATE_COURSE = {
    201: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': {
                    'id': 0,
                    'name': 'Название курса',
                    'description': 'Описание курса'
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

DELETE_COURSE = {
    204: {
        'content': {
            'application/json': {
                'example': ""
            }
        }
    },
    400: {
        'content': {
            'application/json': {
                "example": {"detail": "Данный курс уже закрыт."}
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
