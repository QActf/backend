GET_TARIFFS = {
    200: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': [
                    {
                        'id': 0,
                        'name': 'Название тарифа',
                        'description': 'Описание тарифа'
                    }
                ]
            }
        }
    }
}

GET_TARIFF = {
    200: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': {
                    'id': 0,
                    'name': 'Название тарифа',
                    'description': 'Описание тарифа'
                }
            }
        }
    }
}
UPDATE_TARIFF = {
    200: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': {
                    'id': 0,
                    'name': 'Название тарифа',
                    'description': 'Описание тарифа'
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

CREATE_TARIFF = {
    201: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': {
                    'id': 0,
                    'name': 'Название тарифа',
                    'description': 'Описание тарифа'
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

DELETE_TARIFF = {
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
