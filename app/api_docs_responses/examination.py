from app.api_docs_responses.utils_docs import (get_200_dosc, get_201_dosc,
                                               get_204_dosc, get_401_dosc,
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

GET_EXAMINATIONS = get_200_dosc(content_examenations)

GET_EXAMINATION = {
    **get_200_dosc(content_examenation),
    **get_404_dosc("Объект examination с id 1 не найден.")
}

GET_USER_EXAMINATION = {
    **get_200_dosc(content_examenation),
    **get_401_dosc()
}
GET_USER_EXAMINATIONS = {
    **get_200_dosc(content_examenations),
    **get_401_dosc()
}

CREATE_EXAMINATION = {
    **get_201_dosc(content_examenation),
    **get_401_dosc()
}

DELETE_EXAMINATION = {
    **get_204_dosc(),
    **get_401_dosc()
}
