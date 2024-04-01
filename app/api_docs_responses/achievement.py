from app.api_docs_responses.utils_docs import (get_200_dosc, get_201_dosc,
                                               get_204_dosc, get_401_dosc,
                                               get_403_dosc, get_404_dosc)

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
    **get_200_dosc(content_achievements),
    **get_401_dosc()
}

GET_ACHIEVEMENT = {
    **get_200_dosc(content_achievement),
    **get_401_dosc()
}

GET_ME_ACHIEVEMENT = {
    **get_200_dosc(content_achievements),
    **get_401_dosc(),
    **get_403_dosc("У вас нет этого достижения."),
    **get_404_dosc("Достижение не существует")
}

CREATE_ACHIEVEMENT = {
    **get_201_dosc(content_achievement),
    **get_401_dosc()
}
DELETE_ACHIEVEMENT = {
    **get_204_dosc(),
    **get_401_dosc()
}
