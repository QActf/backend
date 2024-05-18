from app.api_docs_responses.utils_docs import (
    get_200_docs, get_204_docs, get_401_docs, get_403_docs,
    get_404_docs, get_405_docs
)


profile_example = {
    "id": 0,
    "first_name": 'Имя',
    "last_name": 'Фамилия',
    "age": 0,
    "user_id": 0,
    "image": 'Ссылка на изображение'
}

content_profiles = {
    'application/json': {
        'example': [profile_example]
    }
}

content_profile = {
    'application/json': {
        'example': profile_example
    }
}

get_profiles_response = {
    **get_200_docs(content_profiles),
    **get_401_docs(),
}

get_me_profile_response = {
    **get_200_docs(content_profile),
    **get_401_docs(),
}

get_profile_response = {
    **get_200_docs(content_profile),
    **get_401_docs(),
    **get_403_docs("У вас нет доступа к этому профилю."),
    **get_404_docs("Объект profile не найден."),
}

get_profile_photo_response = {
    **get_200_docs(content_profile),
    **get_401_docs(),
}

update_profile_photo_response = {
    **get_200_docs(content_profile),
    **get_401_docs(),
}

update_profile_response = {
    **get_200_docs(content_profile),
    **get_401_docs(),
    **get_403_docs("У вас нет доступа для изменения этого профиля."),
}

create_profile_response = {
    **get_405_docs(
        'Профиль создаётся автоматически при создании пользователя. '
        'Используйте метод PATCH.'
    ),
}

delete_profile_response = {
    **get_204_docs(),
    **get_405_docs('Профиль удаляется при удалении пользователя.'),
}

GET_PROFILES = dict(
    responses=get_profiles_response,
    summary="Получение всех профилей",
    description="""
    ## Получение всех профилей.

    Permissions:
    - Требуется аутентификация на уровне admin.

    Returns:
    - HTTP 200 OK: Если список профилей успешно получен.

    Errors:
    - HTTP 401 Unauthorized: Если пользователь не авторизован.
    """
)

GET_ME_PROFILE = dict(
    responses=get_me_profile_response,
    summary="Получение своего профиля пользователя",
    description="""
    ## Получение информации о своем профиле пользователя.

    Permissions:
    - Требуется аутентификация на уровне user.

    Returns:
    - HTTP 200 OK: Если профиль успешно получен.

    Errors:
    - HTTP 401 Unauthorized: Если пользователь не авторизован.
    """
)

GET_PROFILE = dict(
    responses=get_profile_response,
    summary="Получение профиля пользователя",
    description="""
    ## Получение информации о профиле пользователя по id.

    Permissions:
    - Требуется аутентификация на уровне admin.

    Parameters:
    - `profile_id` (int): Идентификатор профиля, который требуется получить.

    Returns:
    - HTTP 200 OK: Если профиль успешно получен.

    Errors:
    - HTTP 401 Unauthorized: Если пользователь не авторизован.
    - HTTP 403 Forbidden: Если у пользователя нет прав на доступ
    к этому профилю.
    - HTTP 404 Not Found: Если профиль с указанным `profile_id` не существует.
    """
)

GET_PROFILE_PHOTO = dict(
    responses=get_profile_photo_response,
    summary="Получение фото профиля",
    description="""
    ## Получение фото своего профиля пользователя.

    Permissions:
    - Требуется аутентификация на уровне user.

    Returns:
    - HTTP 200 OK: Если фото профиля успешно получено.

    Errors:
    - HTTP 401 Unauthorized: Если пользователь не авторизован.
    """
)

UPDATE_PROFILE_PHOTO = dict(
    responses=update_profile_photo_response,
    summary="Обновление фото профиля",
    description="""
    ## Обновление фото своего профиля пользователя.

    Permissions:
    - Требуется аутентификация на уровне user.

    Returns:
    - HTTP 200 OK: Если фото профиля успешно изменено.

    Errors:
    - HTTP 401 Unauthorized: Если пользователь не авторизован.
    """
)

CREATE_PROFILE = dict(
    responses=create_profile_response,
    summary="Создание профиля",
    description="""
    ## Создание профиля.

    Permissions:
    - Доступно всем

    Errors:
    - HTTP 405 Method Not Allowed: Профиль создаётся автоматически
    при создании пользователя. Используйте метод PATCH.

    Notes:
    - Профиль создаётся автоматически при создании пользователя.
    Используйте метод PATCH.
    """
)

UPDATE_PROFILE = dict(
    responses=update_profile_response,
    summary="Изменение своего профиля",
    description="""
    ## Изменение своего профиля пользователя.

    Permissions:
    - Требуется аутентификация на уровне user.

    Returns:
    - HTTP 200 OK: Если профиль успешно изменен.

    Errors:
    - HTTP 401 Unauthorized: Если пользователь не авторизован.
    - HTTP 403 Forbidden: Если у пользователя нет прав на изменение
    этого профиля.
    """
)

DELETE_PROFILE = dict(
    responses=delete_profile_response,
    summary="Удаление профиля",
    description="""
    ## Удаление профиля пользователя.

    Permissions:
    - Доступно всем.

    Errors:
    - HTTP 405 Method Not Allowed: Профиль удаляется при удалении пользователя.

    Notes:
    -Профиль удаляется при удалении пользователя.
    """
)
