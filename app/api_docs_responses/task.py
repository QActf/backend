from app.api_docs_responses.utils_docs import (get_200_dosc, get_201_dosc,
                                               get_204_dosc, get_401_dosc)

content_tasks = {
    'application/json': {
        'example': [
            {
                'id': 0,
                'name': 'Название задачи',
                'description': 'Описание задачи'
            }
        ]
    }
}

content_task = {
    'application/json': {
        'example': {
            'id': 0,
            'name': 'Название задачи',
            'description': 'Описание задачи'
        }
    }
}

GET_TASKS = {
    **get_200_dosc(content_tasks),
    **get_401_dosc()
}

GET_TASK = {
    **get_200_dosc(content_task),
    **get_401_dosc()
}

CREATE_TASK = {
    **get_201_dosc(content_task),
    **get_401_dosc()
}
DELETE_TASK = {
    **get_204_dosc(),
    **get_401_dosc()
}
