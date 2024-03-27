GET_ACHIEVEMENTS = {
    200: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': [
                    {
                        'id': 0,
                        'name': 'Название достижения',
                        'description': 'Описание достижения'
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

GET_ACHIEVEMENT = {
    200: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': {
                    'id': 0,
                    'name': 'Название достижения',
                    'description': 'Описание достижения'
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

GET_ME_ACHIEVEMENT = {
    200: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': {
                    'id': 0,
                    'name': 'Название достижения',
                    'description': 'Описание достижения'
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
    },
    403: {
        'content': {
            'application/json': {
                "example": {"detail": "У вас нет этого достижения."}
            }
        }
    },
    404: {
        'content': {
            'application/json': {
                "example": {"detail": "Достижение не существует"}
            }
        }
    }
}

CREATE_ACHIEVEMENT = {
    201: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': {
                    'id': 0,
                    'name': 'Название достижения',
                    'description': 'Описание достижения'
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
DELETE_ACHIEVEMENT = {
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
