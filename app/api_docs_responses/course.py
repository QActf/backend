from app.api_docs_responses.utils_docs import (get_200_docs, get_201_docs,
                                               get_204_docs, get_400_docs,
                                               get_401_docs, get_403_docs)

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

GET_COURSES = get_200_docs(content_courses)
GET_USER_COURSES = {
    **get_200_docs(content_courses),
    **get_401_docs()
}
GET_USER_COURSE = {
    **get_200_docs(content_course),
    **get_401_docs(),
    **get_403_docs("Вы не записаны на данный курс.")
}

GET_COURSE = {
    **get_200_docs(content_course),
    **get_401_docs()
}

CREATE_COURSE = {
    **get_201_docs(content_course),
    **get_401_docs()
}

DELETE_COURSE = {
    **get_204_docs(),
    **get_400_docs("Данный курс уже закрыт."),
    **get_401_docs()
}
