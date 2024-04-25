from app.api_docs_responses.utils_docs import (
    get_200_docs, get_201_docs, get_204_docs, get_401_docs, get_404_docs
)

content_examenations = {
    'application/json': {
        'examples': {
            'examenations_with_all_fields': {
                'summary': 'Экзамен со всеми заполнеными полями',
                'value': [{
                    'id': 0,
                    'name': 'Название экзамена.',
                    'description': 'Описание экзамена.'
                }]
            },
            'examenations_without_description': {
                'summary': 'Экзамен без описания',
                'value': [{
                    'id': 0,
                    'name': 'Название экзамена.'
                }]
            }
        }
    }
}
content_examenation = {
    'application/json': {
        'examples': {
            'examenations_with_all_fields': {
                'summary': 'Экзамен со всеми заполнеными полями',
                'value': {
                    'id': 0,
                    'name': 'Название экзамена.',
                    'description': 'Описание экзамена.'
                }
            },
            'examenations_without_description': {
                'summary': 'Экзамен без описания',
                'value': {
                    'id': 0,
                    'name': 'Название экзамена.'
                }
            }
        }
    }
}

GET_EXAMINATIONS = get_200_docs(content_examenations)

GET_EXAMINATION = {
    **get_200_docs(content_examenation),
    **get_404_docs("Объект examination с id 1 не найден.")
}

GET_USER_EXAMINATION = {
    **get_200_docs(content_examenation),
    **get_401_docs()
}
GET_USER_EXAMINATIONS = {
    **get_200_docs(content_examenations),
    **get_401_docs()
}

CREATE_EXAMINATION = {
    **get_201_docs(content_examenation),
    **get_401_docs()
}

DELETE_EXAMINATION = {
    **get_204_docs(),
    **get_401_docs()
}
