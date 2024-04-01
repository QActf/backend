from app.api_docs_responses.utils_docs import get_204_dosc, get_401_dosc

content_tariffs = {
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

content_tariff = {
    'application/json': {
        'example': {
            'id': 0,
            'name': 'Название тарифа',
            'description': 'Описание тарифа'
        }
    }
}

GET_TARIFFS = {
    200: {
        'descripton': 'Success',
        'content': content_tariffs
    }
}

GET_TARIFF = {
    200: {
        'descripton': 'Success',
        'content': content_tariff
    }
}
UPDATE_TARIFF = {
    200: {
        'descripton': 'Success',
        'content': content_tariff
    },
    **get_401_dosc()
}

CREATE_TARIFF = {
    201: {
        'descripton': 'Success',
        'content': content_tariff
    },
    **get_401_dosc()
}

DELETE_TARIFF = {
    **get_204_dosc(),
    **get_401_dosc()
}
