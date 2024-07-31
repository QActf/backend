from sqladmin import ModelView

from app.models import Examination


class ExaminationAdmin(ModelView, model=Examination):
    column_list = [Examination.id, Examination.name, Examination.description]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = 'Examination'
    name_plural = 'Examinations'
    icon = 'fa-solid fa-graduation-cap'
    category = 'training'
    column_searchable_list = [Examination.name]
    column_sortable_list = [Examination.id]
