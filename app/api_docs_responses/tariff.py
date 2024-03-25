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
    }
}