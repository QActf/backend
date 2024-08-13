from app.api_docs_responses.utils_docs import get_200_docs, get_404_docs

questions_with_all_fields = {
    'id': 0,
    'problem': 'Описание проблемы',
    'solution': 'Решение проблемы',
}

questions_without_sulution = {
    'id': 0,
    'problem': 'Описание проблемы',
}

content_questions = {
    'application/json': {
        'examples': {
            'questions_with_all_fields': {
                'summary': 'Вопрос со всеми заполненными полями',
                'value': [questions_with_all_fields],
            },
            'questions_without_sulution': {
                'summary': 'Вопрос без решения',
                'value': [questions_without_sulution],
            }
        }
    }
}

content_question = {
    'application/json': {
        'examples': {
            'question_with_all_fields': {
                'summary': 'Вопрос со всеми заполненными полями',
                'value': questions_with_all_fields,
            },
            'question_without_sulution': {
                'summary': 'Вопрос без решения',
                'value': questions_without_sulution,
            }
        }
    }
}

get_questions_response = {
    **get_200_docs(content_questions),
}

get_question_response = {
    **get_200_docs(content_question),
    **get_404_docs('Объект question не найден.'),
}


GET_QUESTIONS = dict(
    responses=get_questions_response,
    summary='Получение всего списка часто задаваемых вопросов',
    description="""
    ## Получение всех часто задаваемых вопросов.

    Permissions:
    - Для всех пользователей.

    Returns:
    - HTTP 200 OK: Если список часто задаваемых вопросов успешно получен.
    """
)

GET_QUESTION = dict(
    responses=get_question_response,
    summary='Получение часто задаваемого вопроса по ID',
    description="""
    ## Получение информации о вопросе по её идентификатору.

    Permissions:
    - Для всех пользователей.

    Returns:
    - HTTP 200 OK: Если вопрос успешно получен.
    """
)
