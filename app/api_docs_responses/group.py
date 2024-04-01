from app.api_docs_responses.utils_docs import (get_200_dosc, get_201_dosc,
                                               get_204_dosc, get_401_dosc,
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
    **get_200_dosc(content_groups),
    **get_401_dosc()
}

GET_GROUP = {
    **get_200_dosc(content_group),
    **get_401_dosc()
}

GET_USER_GROUP = {
    **get_200_dosc(content_group),
    **get_401_dosc(),
    **get_403_dosc("Вы не состоите в этой группе."),
    **get_404_dosc("Такой группы не существует.")
}

CREATE_GROUP = {
    **get_201_dosc(content_group),
    **get_401_dosc()
}

DELETE_GROUP = {
    **get_204_dosc(),
    **get_401_dosc()
}
