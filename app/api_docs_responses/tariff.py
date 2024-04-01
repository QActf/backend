from app.api_docs_responses.utils_docs import (get_200_dosc, get_201_dosc,
                                               get_204_dosc, get_401_dosc)

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

GET_TARIFFS = get_200_dosc(content_tariffs)
GET_TARIFF = get_200_dosc(content_tariff)
UPDATE_TARIFF = {
    **get_200_dosc(content_tariffs),
    **get_401_dosc()
}

CREATE_TARIFF = {
    **get_201_dosc(content_tariff),
    **get_401_dosc()
}

DELETE_TARIFF = {
    **get_204_dosc(),
    **get_401_dosc()
}
