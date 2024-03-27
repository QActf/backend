def delete_example_value():
    """Пример значения возвращаемого при удалении объекта."""
    return {
        204: {
            'descripton': 'Success',
            'content': {
                'application/json': {
                    'example': ""
                }
            }
        }
    }
