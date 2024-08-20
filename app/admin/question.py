from sqladmin import ModelView

from app.models import Question


class QuestionAdmin(ModelView, model=Question):
    column_list = [Question.id, Question.problem]
    column_searchable_list = [Question.problem]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = 'Question'
    name_plural = 'Questions'
    icon = 'fa-solid fa-question'
    category = 'HELP'
    column_formatters = {Question.problem: lambda m, a: m.problem[:50]}
