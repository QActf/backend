from app.api_docs_responses.utils_docs import (get_204_dosc, get_401_dosc,
                                               get_404_dosc)

content_examenations = {
    'application/json': {
        'example': [
            {
                'id': 0,
                'name': 'Название экзамена.',
                'description': 'Описание экзамена.'
            }
        ]
    }
}
content_examenation = {
    'application/json': {
        'example': {
            'id': 0,
            'name': 'Название экзамена',
                    'description': 'Описание экзамена'
        }
    }
}

GET_EXAMINATIONS = {
    200: {
        'descripton': 'Success',
        'content': content_examenations
    }
}

GET_EXAMINATION = {
    200: {
        'descripton': 'Success',
        'content': content_examenation
    },
    **get_404_dosc("Объект examination с id 1 не найден.")
}

GET_USER_EXAMINATION = {
    200: {
        'descripton': 'Success',
        'content': content_examenations
    },
    **get_401_dosc()
}

CREATE_EXAMINATION = {
    201: {
        'descripton': 'Success',
        'content': content_examenation
    },
    **get_401_dosc()
}

DELETE_EXAMINATION = {
    **get_204_dosc(),
    **get_401_dosc()
}
