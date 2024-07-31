from sqladmin import ModelView

from app.models import Course


class CourseAdmin(ModelView, model=Course):
    column_list = [
        Course.id,
        Course.name,
        Course.description,
        Course.tasks,
        Course.users,
    ]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = 'Course'
    name_plural = 'Courses'
    icon = 'fa-solid fa-book'
    category = 'training'
    column_searchable_list = [Course.name]
    column_sortable_list = [Course.id]
