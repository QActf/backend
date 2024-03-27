GET_EXAMINATIONS = {
    200: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': [
                                {
                                    'id': 0,
                                    'name': 'Название экзамена',
                                    'description': 'Описание экзамена'
                                }
                ]
            }
        }
    }
}

GET_EXAMINATION = {
    200: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': {
                    'id': 0,
                    'name': 'Название экзамена',
                    'description': 'Описание экзамена'
                }
            }
        }
    },
    404: {
        'content': {
            'application/json': {
                "example": {"detail": "Объект examination с id 1 не найден."}
            }
        }
    }
}

GET_USER_EXAMINATION = {
    200: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': {
                    'id': 0,
                    'name': 'Название экзамена',
                    'description': 'Описание экзамена'
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

CREATE_EXAMINATION = {
    201: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': {
                    'id': 0,
                    'name': 'Название экзамена',
                    'description': 'Описание экзамена'
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

DELETE_EXAMINATION = {
    204: {
        'content': {
            'application/json': {
                'example': ""
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
