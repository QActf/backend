from app.api_docs_responses.utils_docs import (get_204_dosc, get_401_dosc,
                                               get_403_dosc, get_404_dosc)

content_achievements = {
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
content_achievement = {
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

GET_ACHIEVEMENTS = {
    200: {
        'descripton': 'Success',
        'content': content_achievements
    },
    **get_401_dosc()
}

GET_ACHIEVEMENT = {
    200: {
        'descripton': 'Success',
        'content': content_achievement
    },
    **get_401_dosc()
}

GET_ME_ACHIEVEMENT = {
    200: {
        'descripton': 'Success',
        'content': content_achievements
    },
    **get_401_dosc(),
    **get_403_dosc("У вас нет этого достижения."),
    **get_404_dosc("Достижение не существует")
}

CREATE_ACHIEVEMENT = {
    201: {
        'descripton': 'Success',
        'content': content_achievement
    },
    **get_401_dosc()
}
DELETE_ACHIEVEMENT = {
    **get_204_dosc(),
    **get_401_dosc()
}
