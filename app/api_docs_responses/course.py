from app.api_docs_responses.utils_docs import (get_200_docs, get_201_docs,
                                               get_204_docs, get_400_docs,
                                               get_401_docs, get_403_docs)

courses_with_all_fields = {
    'id': 0,
    'name': 'Название курса',
    'description': 'Описание курса'
}

courses_without_description = {
    'id': 0,
    'name': 'Название курса'
}

content_courses = {
    'application/json': {
        'examples': {
            'courses_with_all_fields': {
                'summary': 'Курс со всеми заполненными полями',
                'value': [courses_with_all_fields]
            },
            'courses_without_description': {
                'summary': 'Курс без описания',
                'value': [courses_without_description]
            }
        }
    }
}

content_course = {
    'application/json': {
        'examples': {
            'course_with_all_fields': {
                'summary': 'Курс со всеми заполненными полями',
                'value': courses_with_all_fields
            },
            'course_without_description': {
                'summary': 'Достижение без описания',
                'value': courses_without_description
            }
        }
    }
}

get_courses_response = get_200_docs(content_courses)
get_user_courses_response = {
    **get_200_docs(content_courses),
    **get_401_docs()
}
get_user_course_response = {
    **get_200_docs(content_course),
    **get_401_docs(),
    **get_403_docs("Вы не записаны на данный курс.")
}

get_course_response = {
    **get_200_docs(content_course),
    **get_401_docs()
}

create_course_response = {
    **get_201_docs(content_course),
    **get_401_docs()
}

delete_course_response = {
    **get_204_docs(),
    **get_400_docs("Данный курс уже закрыт."),
    **get_401_docs()
}

GET_COURSES = dict(
    responses=get_courses_response,
    summary="Получение всех курсов",
)

GET_USER_COURSES = dict(
    responses=get_user_courses_response,
    summary="Получение курсов пользователя",
)

GET_USER_COURSE = dict(
    responses=get_user_course_response,
    summary="Получение курса пользователя",
)

GET_COURSE = dict(
    responses=get_course_response,
    summary="Получение курса",
)

PATCH_COURSE = dict(
    responses = get_course_response,
    summary = "Изменение курса",
)

CREATE_COURSE = dict(
    responses=create_course_response,
    summary="Создание курса",
)

DELETE_COURSE = dict(
    responses=delete_course_response,
    summary="Удаление курса",
)