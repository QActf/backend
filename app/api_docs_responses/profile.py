from app.api_docs_responses.utils_docs import (get_200_dosc, get_204_dosc,
                                               get_401_dosc, get_405_dosc)

content_profiles = {
    'application/json': {
        'example': [
            {
                "id": 0,
                "first_name": 'Имя',
                "last_name": 'Фамилия',
                "age": 0,
                "user_id": 0,
                "image": 'Ссылка на изображение'
            }
        ]
    }
}
content_profile = {
    'application/json': {
        'example': {
            "id": 0,
            "first_name": 'Имя',
            "last_name": 'Фамилия',
            "age": 0,
            "user_id": 0,
            "image": 'Ссылка на изображение'
        }

    }
}

GET_PROFILES = {
    **get_200_dosc(content_profiles),
    **get_401_dosc()
}

GET_PROFILE = {
    **get_200_dosc(content_profile),
    **get_401_dosc()
}
GET_PROFILE_PHOTO = {
    200: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': 'Ссылка на изображение'
            }
        }
    },
    **get_401_dosc()
}
CREATE_PROFILE = {
    **get_200_dosc(content_profile),
    **get_405_dosc("Профиль создаётся автоматически при "
                   "создании пользователя. Используйте метод PATCH.")
}
DELETE_PROFILE = {
    **get_204_dosc(),
    **get_405_dosc("Профиль удаляется при удалении пользователя.")
}
