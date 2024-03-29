GET_TASKS = {
    200: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': [
                    {
                        'id': 0,
                        'name': 'Название задачи',
                        'description': 'Описание задачи'
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

GET_TASK = {
    200: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': {
                    'id': 0,
                    'name': 'Название задачи',
                    'description': 'Описание задачи'
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

CREATE_TASK = {
    201: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': {
                    'id': 0,
                    'name': 'Название задачи',
                    'description': 'Описание задачи'
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
DELETE_TASK = {
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
