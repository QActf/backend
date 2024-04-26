from app.api_docs_responses.utils_docs import (
    get_200_docs, get_204_docs, get_401_docs, get_405_docs
)

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
    **get_200_docs(content_profiles),
    **get_401_docs()
}

GET_PROFILE = {
    **get_200_docs(content_profile),
    **get_401_docs()
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
    **get_401_docs()
}
CREATE_PROFILE = {
    **get_200_docs(content_profile),
    **get_405_docs("Профиль создаётся автоматически при "
                   "создании пользователя. Используйте метод PATCH.")
}
DELETE_PROFILE = {
    **get_204_docs(),
    **get_405_docs("Профиль удаляется при удалении пользователя.")
}
