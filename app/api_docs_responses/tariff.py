from app.api_docs_responses.utils_docs import (
    get_200_docs, get_201_docs, get_204_docs, get_401_docs
)

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

ALL_TARIFFS_DECRIPTION = """
    Получение всех тарифов, который есть в БД.

    Args:\n
        tariff_id (int): Идентификатор тарифа.\n
    Returns:\n
        list: dict(Информация о тарифе).\n
    Permissions:\n
        Доступно всем.
"""

TARIFF_ID_DESCRIPTION = """
    Получение тарифа по его id или
    получение ошибки 404 в случае отсутствия данного тарифа.

    Args:\n
        tariff_id (int): Идентификатор тарифа.\n
    Returns:\n
        dict: Информация о тарифе.\n
    Permissions:\n
        Доступно всем.
"""

TARIFF_ID_PATCH_ODESCRIPTION = """
    Частичное обновление информации о тарифе по его идентификатору.

    Args:\n
        tariff_id (int): Идентификатор тарифа.\n
        data (TariffUpdate): Данные для обновления.\n
    Returns:\n
        dict: Информация о тарифе.\n
    Permissions:\n
"""

TARIFF_CREATE_DESCRIPTION = """
    Создание тарифа.

    Args:\n
        tariff(dict): Данные нового тарифа.\n
        data (TariffUpdate): Данные для обновления.\n
    Returns:\n
        dict: Новый тариф.\n
    Permissions:\n
        Только суперпользователь.\n
"""

TARIFF_ID_DELETE = """
    Удаление тарифа по его идентификатору.

    Args:\n
        tariff(dict): Данные нового тарифа.\n
        data (TariffUpdate): Данные для обновления.\n
    Returns:\n
        dict: Новый тариф.\n
    Permissions:\n
        Только суперпользователь.\n
"""
