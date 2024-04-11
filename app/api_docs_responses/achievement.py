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
