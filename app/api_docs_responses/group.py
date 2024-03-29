from app.api_docs_responses.utils_docs import (get_204_dosc, get_401_dosc,
                                               get_403_dosc, get_404_dosc)

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
    200: {
        'description': 'Success',
        'content': content_groups
    },
    **get_401_dosc()
}

GET_GROUP = {
    200: {
        'descripton': 'Success',
        'content': content_group
    },
    **get_401_dosc()
}

GET_USER_GROUP = {
    200: {
        'descripton': 'Success',
        'content': content_groups
    },
    **get_401_dosc(),
    **get_403_dosc("Вы не состоите в этой группе."),
    **get_404_dosc("Такой группы не существует.")
}

CREATE_GROUP = {
    201: {
        'descripton': 'Success',
        'content': content_group
    },
    **get_401_dosc()
}

DELETE_GROUP = {
    **get_204_dosc(),
    **get_401_dosc()
}
