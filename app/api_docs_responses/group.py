from app.api_docs_responses.utils_docs import (get_200_docs, get_201_docs,
                                               get_204_docs, get_401_docs,
                                               get_403_docs, get_404_docs)

content_groups = {
    'application/json': {
        'examples': {
            'group_with_all_fields': {
                'summary': 'Группа со всеми заполнеными полями',
                'value': [{
                    'id': 0,
                    'name': 'Название группы',
                    'description': 'Описание группы'
                }]
            },
            'group_without_description': {
                'summary': 'Группа без описания',
                'value': [{
                    'id': 0,
                    'name': 'Название группы'
                }]
            }
        }
    }
}

content_group = {
    'application/json': {
        'examples': {
            'group_with_all_fields': {
                'summary': 'Группа со всеми заполнеными полями',
                'value': {
                    'id': 0,
                    'name': 'Название группы',
                    'description': 'Описание группы'
                }
            },
            'group_without_description': {
                'summary': 'Группа без описания',
                'value': {
                    'id': 0,
                    'name': 'Название группы'
                }
            }
        }
    }
}

GET_GROUPS = {
    **get_200_docs(content_groups),
    **get_401_docs()
}

GET_GROUP = {
    **get_200_docs(content_group),
    **get_401_docs()
}

GET_USER_GROUP = {
    **get_200_docs(content_group),
    **get_401_docs(),
    **get_403_docs("Вы не состоите в этой группе."),
    **get_404_docs("Такой группы не существует.")
}

CREATE_GROUP = {
    **get_201_docs(content_group),
    **get_401_docs()
}

DELETE_GROUP = {
    **get_204_docs(),
    **get_401_docs()
}
