from app.api_docs_responses.utils_docs import (get_200_docs, get_201_docs,
                                               get_204_docs, get_400_docs,
                                               get_401_docs, get_404_docs)

tasks_with_all_fields = {
    'id': 0,
    'name': 'Название задачи',
    'description': 'Описание задачи',
}

tasks_without_description = {
    'id': 0,
    'name': 'Название задачи',
}

content_tasks = {
    'application/json': {
        'examples': {
            'tasks_with_all_fields': {
                'summary': 'Задача со всеми заполненными полями',
                'value': [tasks_with_all_fields],
            },
            'tasks_without_description': {
                'summary': 'Задача без описания',
                'value': [tasks_without_description],
            }
        }
    }
}

content_task = {
    'application/json': {
        'examples': {
            'task_with_all_fields': {
                'summary': 'Задача со всеми заполненными полями',
                'value': tasks_with_all_fields,
            },
            'task_without_description': {
                'summary': 'Задача без описания',
                'value': tasks_without_description,
            }
        }
    }
}

get_tasks_response = {
    **get_200_docs(content_tasks),
    **get_401_docs(),
}

get_task_response = {
    **get_200_docs(content_task),
    **get_401_docs(),
}

create_task_response = {
    **get_201_docs(content_task),
    **get_401_docs(),
}

update_task_response = {
    **get_200_docs(content_task),
    **get_401_docs(),
    **get_400_docs("Объект tasks с таким именем уже существует!"),
    **get_404_docs("Объект tasks не найден."),
}

delete_task_response = {
    **get_204_docs(),
    **get_401_docs(),
    **get_404_docs("Объект tasks не найден."),
}

GET_TASKS = dict(
    responses=get_tasks_response,
    summary="Получение всех задач",
    description="""
    ## Получение всех задач.

    Permissions:
    - Требуется аутентификация на уровне admin.

    Returns:
    - HTTP 200 OK: Если список задач успешно получен.
    - HTTP 401 Unauthorized: Если пользователь не авторизован.
    """
)

GET_TASK = dict(
    responses=get_task_response,
    summary="Получение задачи",
    description="""
    ## Получение информации о задаче по её идентификатору.

    Permissions:
    - Требуется аутентификация на уровне admin.

    Returns:
    - HTTP 200 OK: Если задача успешно получена.
    - HTTP 401 Unauthorized: Если пользователь не авторизован.
    """
)

CREATE_TASK = dict(
    responses=create_task_response,
    summary="Создание задачи",
    description="""
    ## Создание новой задачи.

    Permissions:
    - Требуется аутентификация на уровне admin.

    Returns:
    - HTTP 201 Created: Если задача успешно создана.
    - HTTP 400 Bad Request: Если попытка создания задачи невозможна,
    потому что задача с таким именем уже создан.
    - HTTP 401 Unauthorized: Если пользователь не авторизован.
    """
)

PATCH_TASK = dict(
    responses=update_task_response,
    summary="Изменение задачи",
    description="""
    ## Изменение информации о задаче по её идентификатору.

    Permissions:
    - Требуется аутентификация на уровне admin.

    Parameters:
    - `task_id` (int): Идентификатор задачи, который требуется изменить.

    Returns:
    - HTTP 200 OK: Если информация о задачи успешно изменена.

    Raises:
    - HTTP 401 Unauthorized: Если пользователь не авторизован.
    - HTTP 403 Forbidden: Если у пользователя нет прав на изменение
    данной задачи или задача не существует.
    - HTTP 404 Not Found: Если задача с указанным `task_id` не существует.
    """
)

DELETE_TASK = dict(
    responses=delete_task_response,
    summary="Удаление задачи",
    description="""
    ## Удаление задачи по её идентификатору.

    Permissions:
    - Требуется аутентификация на уровне admin.

    Returns:
    - HTTP 204 No Content: Если задача успешно удалена.
    - HTTP 401 Unauthorized: Если пользователь не авторизован.
    - HTTP 404 Not Found: Если задача с `task_id` не существует.
    """
)
