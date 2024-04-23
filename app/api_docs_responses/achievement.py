from app.api_docs_responses.utils_docs import (get_200_docs, get_201_docs,
                                               get_204_docs, get_401_docs,
                                               get_403_docs, get_404_docs)

content_achievements = {
    'application/json': {
        'examples': {
            'achievement_with_all_fields': {
                'summary': 'Достижение со всеми заполнеными полями',
                'value': [{
                    'id': 0,
                    'name': 'Название достижения',
                    'description': 'Описание достижения'
                }]
            },
            'achievement_without_description': {
                'summary': 'Достижение без описания',
                'value': [{
                    'id': 0,
                    'name': 'Название достижения',
                }]
            }
        }
    }
}
content_achievement = {
    'application/json': {
        'examples': {
            'achievement_with_all_fields': {
                'summary': 'Достижение со всеми заполнеными полями',
                'value': {
                    'id': 0,
                    'name': 'Название достижения',
                    'description': 'Описание достижения'
                }
            },
            'achievement_without_description': {
                'summary': 'Достижение без описания',
                'value': {
                    'id': 0,
                    'name': 'Название достижения',
                }
            }
        }
    }
}

GET_ACHIEVEMENTS = {
    **get_200_docs(content_achievements),
    **get_401_docs()
}

GET_ACHIEVEMENT = {
    **get_200_docs(content_achievement),
    **get_401_docs()
}

GET_ME_ACHIEVEMENT = {
    **get_200_docs(content_achievements),
    **get_401_docs(),
    **get_403_docs("У вас нет этого достижения."),
    **get_404_docs("Достижение не существует")
}

CREATE_ACHIEVEMENT = {
    **get_201_docs(content_achievement),
    **get_401_docs()
}
DELETE_ACHIEVEMENT = {
    **get_204_docs(),
    **get_401_docs()
}

GET_ALL_ACHIEVEMENTS_DESCRIPTION = """
Получение всех достижений, которые есть в БД.\n
    Args:\n
        None\n
    Returns:\n
        list: dict(Информация о достижении).\n
    Permissions:\n
        Доступно только суперпользователю.
"""

GET_ACHIEVEMENTS_CURRENTUSER_DESCRIPTION = """
Получение достижений текущего пользователя.\n
    Args:\n
        None\n
    Returns:\n
        list: dict(Информация о достижении).\n
    Permissions:\n
        Доступно только текущему пользователю.
"""

GET_ACHIEVEMENT_CURRENTUSER_ID_DESCRIPTION = """
Получение описания достижения пользователя по id.\n
    Args:\n
        achievement_id\n
    Returns:\n
        dict: Информация о запрашиваемом достижении.\n
    Permissions:\n
        Доступно только текущему пользователю.
"""

CREATE_ACHIEVEMENT_DESCRIPTION = """
Cоздание нового достижения,
которое может быть у любого пользователя.\n
    Args:\n
        None\n
    Returns:\n
        dict: Информация о созданно достижении.\n
    Permissions:\n
        Доступно только суперпользователю.
"""

PATCH_ACHIEVEMENT_ID_DESCRIPTION = """
Редактирование существующего достижения в БД.\n
    Args:\n
        achievement_id\n
    Returns:\n
        dict: Информация о достижении после редактирования.\n
    Permissions:\n
        Доступно только суперпользователю.
"""

DELETE_ACHIEVEMENT_DESCRIPTION = """
Удаление существующего достижения в БД.\n
    Args:\n
        achievement_id\n
    Returns:\n
        None\n
    Permissions:\n
        Доступно только суперпользователю.
"""
