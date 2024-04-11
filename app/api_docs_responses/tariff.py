from app.api_docs_responses.utils_docs import (get_200_docs, get_201_docs,
                                               get_204_docs, get_401_docs)

content_tariffs = {
    'application/json': {
        'examples': {
            'tariffs_with_all_fields': {
                'summary': 'Тариф со всеми заполнеными полями',
                'value': [{
                    'id': 0,
                    'name': 'Название тарифа',
                    'description': 'Описание тарифа'
                }]
            },
            'tariffs_without_description': {
                'summary': 'Тариф без описания',
                'value': [{
                    'id': 0,
                    'name': 'Название тарифа'
                }]
            }
        }
    }
}

content_tariff = {
    'application/json': {
        'examples': {
            'tariff_with_all_fields': {
                'summary': 'Тариф со всеми заполнеными полями',
                'value': {
                    'id': 0,
                    'name': 'Название тарифа',
                    'description': 'Описание тарифа'
                }
            },
            'tariff_without_description': {
                'summary': 'Тариф без описания',
                'value': {
                    'id': 0,
                    'name': 'Название тарифа'
                }
            }
        }
    }
}

GET_TARIFFS = get_200_docs(content_tariffs)
GET_TARIFF = get_200_docs(content_tariff)
UPDATE_TARIFF = {
    **get_200_docs(content_tariffs),
    **get_401_docs()
}

CREATE_TARIFF = {
    **get_201_docs(content_tariff),
    **get_401_docs()
}

DELETE_TARIFF = {
    **get_204_docs(),
    **get_401_docs()
}
