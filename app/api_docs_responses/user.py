from app.api_docs_responses.utils_docs import get_204_dosc, get_405_dosc

DELETE_USER = {
    **get_204_dosc(),
    **get_405_dosc("Удаление пользователей запрещено!")
}
