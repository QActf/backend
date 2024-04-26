from app.api_docs_responses.utils_docs import (
    get_200_docs, get_201_docs, get_204_docs, get_401_docs
)

content_tasks = {
    'application/json': {
        'examples': {
            'tasks_with_all_fields': {
                'summary': 'Задача со всеми заполнеными полями',
                'value': [{
                    'id': 0,
                    'name': 'Название задачи',
                    'description': 'Описание задачи'
                }]
            },
            'tasks_without_description': {
                'summary': 'Задача без описания',
                'value': [{
                    'id': 0,
                    'name': 'Название задачи'
                }]
            }
        }
    }
}

content_task = {
    'application/json': {
        'examples': {
            'task_with_all_fields': {
                'summary': 'Задача со всеми заполнеными полями',
                'value': {
                    'id': 0,
                    'name': 'Название задачи',
                    'description': 'Описание задачи'
                }
            },
            'task_without_description': {
                'summary': 'Задача без описания',
                'value': {
                    'id': 0,
                    'name': 'Название задачи'
                }
            }
        }
    }
}

GET_TASKS = {
    **get_200_docs(content_tasks),
    **get_401_docs()
}

GET_TASK = {
    **get_200_docs(content_task),
    **get_401_docs()
}

CREATE_TASK = {
    **get_201_docs(content_task),
    **get_401_docs()
}
DELETE_TASK = {
    **get_204_docs(),
    **get_401_docs()
}
