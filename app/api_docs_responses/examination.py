from app.api_docs_responses.utils_docs import (
    get_200_docs, get_201_docs, get_204_docs,
    get_400_docs, get_401_docs, get_404_docs,
)

examenations_with_all_fields = {
    'id': 0,
    'name': 'Название экзамена.',
    'description': 'Описание экзамена.'
}

examenations_without_description = {
    'id': 0,
    'name': 'Название экзамена.'
}

content_examenations = {
    'application/json': {
        'examples': {
            'examenations_with_all_fields': {
                'summary': 'Экзамен со всеми заполнеными полями',
                'value': [examenations_with_all_fields]
            },
            'examenations_without_description': {
                'summary': 'Экзамен без описания',
                'value': [examenations_without_description]
            }
        }
    }
}
content_examenation = {
    'application/json': {
        'examples': {
            'examenations_with_all_fields': {
                'summary': 'Экзамен со всеми заполнеными полями',
                'value': examenations_with_all_fields
            },
            'examenations_without_description': {
                'summary': 'Экзамен без описания',
                'value': examenations_without_description
            }
        }
    }
}

get_examinations_response = get_200_docs(content_examenations)

get_examination_response = {
    **get_200_docs(content_examenation),
    **get_404_docs("Объект examination не найден."),
}

get_user_examinations_response = {
    **get_200_docs(content_examenations),
    **get_401_docs(),
}

create_examination_response = {
    **get_201_docs(content_examenation),
    **get_400_docs("Объект examination с таким именем уже существует!"),
    **get_401_docs(),
}

update_examination_response = {
    **get_200_docs(content_examenation),
    **get_400_docs("Объект examination с таким именем уже существует!"),
    **get_404_docs("Объект examination не найден."),
}

delete_examination_response = {
    **get_204_docs(),
    **get_401_docs(),
}

GET_EXAMINATIONS = dict(
    responses=get_examinations_response,
    summary="Получение всех экзаменов",
    description="""
    ## Получение всех экзаменов.

    Permissions:
    - Доступно всем.

    Returns:
    - HTTP 200 OK: Если список экзаменов успешно получен.
    """
)

GET_EXAMINATION = dict(
    responses=get_examination_response,
    summary="Получение информации об экзамене",
    description="""
    ## Получение информации об экзамене по его идентификатору.

    Permissions:
    - Доступно всем.

    Parameters:
    - `examination_id` (int): Идентификатор экзамена,
    который требуется изменить.

    Returns:
    - HTTP 200 OK: Если экзамен успешно получен.

    Errors:
    - HTTP 404 Not Found: Если экзамен с указанным `examination_id`
    не существует.
    """
)

GET_USER_EXAMINATIONS = dict(
    responses=get_user_examinations_response,
    summary="Получение экзаменов пользователя",
    description="""
    ## Получение экзаменов, на которые записан текущий пользователь.

    Permissions:
    - Требуется аутентификация на уровне user.

    Returns:
    - HTTP 200 OK: Если список экзаменов успешно получен.

    Errors:
    - HTTP 401 Unauthorized: Если пользователь не авторизован.
    """
)

CREATE_EXAMINATION = dict(
    responses=create_examination_response,
    summary="Создание экзамена",
    description="""
    ## Создание нового экзамена в системе.

    Permissions:
    - Требуется аутентификация на уровне admin.

    Returns:
    - HTTP 201 Created: Если экзамен успешно создан.

    Errors:
    - HTTP 400 Bad Request: Если попытка создания экзамена невозможна,
    потому что экзамен уже с таким именем уже создан.
    - HTTP 401 Unauthorized: Если пользователь не авторизован.
    """
)

UPDATE_EXAMINATION = dict(
    responses=update_examination_response,
    summary="Изменение экзамена",
    description="""
    ## Изменение информации об экзамене по его идентификатору.

    Permissions:
    - Требуется аутентификация на уровне admin.

    Parameters:
    - `examination_id` (int): Идентификатор экзамена,
    который требуется изменить.

    Returns:
    - HTTP 200 OK: Если информация об экзамене успешно изменена.

    Errors:
    - HTTP 400 Bad Request: Если попытка изменения экзамена невозможна,
    потому что экзамен с таким именем уже существует.
    - HTTP 404 Not Found: Если экзамен с указанным `examination_id`
    не существует.
    """
)

DELETE_EXAMINATION = dict(
    responses=delete_examination_response,
    summary="Удаление экзамена",
    description="""
    ## Удаление экзамена.

    Permissions:
    - Требуется аутентификация на уровне admin.

    Parameters:
    - `examination_id` (int): Идентификатор экзамена,
    который требуется удалить.

    Returns:
    - HTTP 204 No Content: Если экзамен успешно удален.

    Errors:
    - HTTP 401 Unauthorized: Если пользователь не авторизован.
    """
)
