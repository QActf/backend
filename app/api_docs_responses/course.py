from app.api_docs_responses.utils_docs import (get_204_dosc, get_400_dosc,
                                               get_401_dosc, get_403_dosc)

content_courses = {
    'application/json': {
        'example': [
            {
                'id': 0,
                'name': 'Название курса',
                'description': 'Описание курса'
            }
        ]
    }
}

content_course = {
    'application/json': {
        'example': {
            'id': 0,
            'name': 'Название курса',
            'description': 'Описание курса'
        }
    }
}

GET_COURSES = {
    200: {
        'descripton': 'Success',
        'content': content_courses
    }
}
GET_USER_COURSES = {
    200: {
        'descripton': 'Success',
        'content': content_courses
    },
    **get_401_dosc()
}
GET_USER_COURSE = {
    200: {
        'descripton': 'Success',
        'content': content_course
    },
    **get_401_dosc(),
    **get_403_dosc("Вы не записаны на данный курс.")
}

GET_COURSE = {
    200: {
        'descripton': 'Success',
        'content': content_course
    },
    **get_401_dosc()
}

CREATE_COURSE = {
    201: {
        'descripton': 'Success',
        'content': content_course
    },
    **get_401_dosc()
}

DELETE_COURSE = {
    **get_204_dosc(),
    **get_400_dosc("Данный курс уже закрыт."),
    **get_401_dosc()
}
