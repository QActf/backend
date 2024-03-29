'''Переменные и функции которые влияют только на отображение документации
 и не влияют на работу программы.
'''


NAME_AND_DESCRIPTION_VALUE = {"name": "Название", "description": "Описание"}
PROFILE_UPDATE_VALUE = {"first_name": "Имя", "last_name": "Фамилия", "age": 20}
USER_VALUE = {
  "password": "Пароль",
  "email": "user@example.com",
  "is_active": True,
  "is_superuser": True,
  "is_verified": True,
  "role": "user",
  "username": "Имя"
}


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
