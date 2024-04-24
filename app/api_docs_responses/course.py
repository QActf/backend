from app.api_docs_responses.utils_docs import (get_200_docs, get_201_docs,
                                               get_400_docs, get_401_docs,
                                               get_403_docs, get_404_docs)


def get_custom_204_docs():
    return {
        204: {
            'description': 'Запись удалена.',
            'content': {
                'application/json': {
                    'example': {
                        'course': 'Название закрытого курса',
                        'message': 'Курс успешно закрыт'
                    }
                }
            }
        }
    }


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
    **get_401_docs(),
}
get_user_course_response = {
    **get_200_docs(content_course),
    **get_401_docs(),
    **get_403_docs("Вы не записаны на данный курс."),
    **get_404_docs("Объект course не найден.."),
}

get_course_response = {
    **get_200_docs(content_course),
    **get_404_docs("Объект course не найден."),
}

update_course_response = {
    **get_200_docs(content_course),
    **get_404_docs("Объект course не найден."),
    **get_400_docs("Объект course с таким именем уже существует!"),
}

create_course_response = {
    **get_201_docs(content_course),
    **get_400_docs("Объект course с таким именем уже существует!"),
}

delete_course_response = {
    **get_custom_204_docs(),
    **get_400_docs("Данный курс уже закрыт."),
    **get_401_docs(),
}

GET_COURSES = dict(
    responses=get_courses_response,
    summary="Получение всех курсов",
    description="""
    ## Получение всех курсов.

    Permissions:
    - Доступно всем.

    Returns:
    - HTTP 200 OK: Если список курсов успешно получен.
    """
)

GET_USER_COURSES = dict(
    responses=get_user_courses_response,
    summary="Получение курсов пользователя",
    description="""
    ## Получение курсов, на которые записан текущий пользователь.

    Permissions:
    - Требуется аутентификация на уровне user.

    Returns:
    - HTTP 200 OK: Если список курсов успешно получен.
    """
)

GET_USER_COURSE = dict(
    responses=get_user_course_response,
    summary="Получение курса пользователя",
    description="""
    ## Получение информации о курсе, на который записан текущий пользователь.

    Permissions:
    - Требуется аутентификация на уровне user.

    Returns:
    - HTTP 200 OK: Если курс успешно получен.

    Errors:
    - HTTP 404 Not Found: Если курс с указанным `course_id` не существует.
    """
)

GET_COURSE = dict(
    responses=get_course_response,
    summary="Получение курса",
    description="""
    ## Получение информации о курсе по его идентификатору.
    Permissions:
    - Доступно всем.

    Returns:
    - HTTP 200 OK: Если курс успешно получен.

    Errors:
    - HTTP 404 Not Found: Если курс с указанным `course_id` не существует.
    """
)

CREATE_COURSE = dict(
    responses=create_course_response,
    summary="Создание курса",
    description="""
    ## Создание нового курса в системе.

    Permissions:
    - Требуется аутентификация ну уровне admin.

    Returns:
    - HTTP 200 OK: Если курс успешно создан.

    Errors:
    - HTTP 400 Bad Request: Если попытка создания курса невозможна,
    потому что курс уже с таким именем уже создан.
    - HTTP 401 Unauthorized: Если пользователь не авторизован.
    """
)

PATCH_COURSE = dict(
    responses=get_course_response,
    summary="Изменение курса",
    description="""
    ## Изменение информации о курсе по его идентификатору.

    Permissions:
    - Требуется аутентификация ну уровне admin.

    Parameters:
    - `course_id` (int): Идентификатор курса, который требуется изменить.

    Returns:
    - HTTP 200 OK: Если информация о курсе успешно изменена.

    Raises:
    - HTTP 401 Unauthorized: Если пользователь не авторизован.
    - HTTP 403 Forbidden: Если у пользователя нет прав на изменение
    данного курса или курс не существует.
    - HTTP 404 Not Found: Если курс с указанным `course_id` не существует.
    """
)

DELETE_COURSE = dict(
    responses=delete_course_response,
    summary="Удаление курса",
    description="""
    ## Удаляет курс.

    Permissions:
    - Требуется аутентификация ну уровне admin.

    Parameters:
    - `course_id` (int): Идентификатор курса, который требуется закрыть.

    Returns:
    - HTTP 204 No Content: Если курс успешно закрыт.

    Raises:
    - HTTP 400 Bad Request: Если попытка закрытия курса невозможна,
    потому что курс уже закрыт.
    - HTTP 404 Not Found: Если курс с закрытие `course_id` не существует.

    Notes:
    - Нельзя удалить курс, если у него уже есть пользователи,
    можно лишь закрыть доступ новым пользователям.
    """
)
