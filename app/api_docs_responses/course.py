from app.api_docs_responses.utils_docs import (get_200_dosc, get_201_dosc,
                                               get_204_dosc, get_400_dosc,
                                               get_401_dosc, get_403_dosc)

content_courses = {
    'application/json': {
        'examples': {
            'courses_with_all_fields': {
                'summary': 'Курс со всеми заполнеными полями',
                'value': [{
                    'id': 0,
                    'name': 'Название курса',
                    'description': 'Описание курса'
                }]
            },
            'courses_without_description': {
                'summary': 'Курс без описания',
                'value': [{
                    'id': 0,
                    'name': 'Название курса',
                }]
            }
        }
    }
}

content_course = {
    'application/json': {
        'examples': {
            'course_with_all_fields': {
                'summary': 'Курс со всеми заполнеными полями',
                'value': {
                    'id': 0,
                    'name': 'Название курса',
                    'description': 'Описание курса'
                }
            },
            'course_without_description': {
                'summary': 'Достижение без описания',
                'value': {
                    'id': 0,
                    'name': 'Название курса',
                }
            }
        }
    }
}

GET_COURSES = get_200_dosc(content_courses)
GET_USER_COURSES = {
    **get_200_dosc(content_courses),
    **get_401_dosc()
}
GET_USER_COURSE = {
    **get_200_dosc(content_course),
    **get_401_dosc(),
    **get_403_dosc("Вы не записаны на данный курс.")
}

GET_COURSE = {
    **get_200_dosc(content_course),
    **get_401_dosc()
}

CREATE_COURSE = {
    **get_201_dosc(content_course),
    **get_401_dosc()
}

DELETE_COURSE = {
    **get_204_dosc(),
    **get_400_dosc("Данный курс уже закрыт."),
    **get_401_dosc()
}
