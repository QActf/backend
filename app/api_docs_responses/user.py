DELETE_USER = {
    204: {
        'content': {
            'application/json': {
                'example': ""
            }
        }
    },
    405: {
        'descripton': 'Success',
        'content': {
            'application/json': {
                "example": {
                    "detail": "Удаление пользователей запрещено!"
                }
            }
        }
    }
}
