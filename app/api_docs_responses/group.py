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
    },
    401: {
        'content': {
            'application/json': {
                "example": {"detail": "Unauthorized"}
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
    },
    401: {
        'content': {
            'application/json': {
                "example": {"detail": "Unauthorized"}
            }
        }
    }
}

GET_USER_GROUP = {
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
    },
    401: {
        'content': {
            'application/json': {
                "example": {"detail": "Unauthorized"}
            }
        }
    },
    403: {
        'content': {
            'application/json': {
                "example": {"detail": "Вы не состоите в этой группе."}
            }
        }
    },
    404: {
        'content': {
            'application/json': {
                "example": {"detail": "Такой группы не существует."}
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
    },
    401: {
        'content': {
            'application/json': {
                "example": {"detail": "Unauthorized"}
            }
        }
    }
}

DELETE_GROUP = {
    204: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                'example': ""
            }
        }
    },
    401: {
        'content': {
            'application/json': {
                "example": {"detail": "Unauthorized"}
            }
        }
    }
}
