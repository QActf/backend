GET_GROUPS = {
    200: {
        'description': 'Success',
        'content': {
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
    }
}

GET_GROUP = {
    200: {
        'descripton': 'Success',
        'content': {
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
    }
}

CREATE_GROUP = {
    201: {
        'descripton': 'Success',
        'content': {
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
    }
}
UPDATE_GROUP = {
    200: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': {
                    'id': 0,
                    'name': 'Название группы',
                    'description': 'Описание группы'
                }
            }
        }
    }
}