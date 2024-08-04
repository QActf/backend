from sqladmin import ModelView

from app.models import Task


class TaskAdmin(ModelView, model=Task):
    column_list = [Task.id, Task.name, Task.courses]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = 'Task'
    name_plural = 'Tasks'
    icon = 'fa-solid fa-list-check'
    category = 'TRAINING'
