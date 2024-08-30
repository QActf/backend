from sqladmin import ModelView

from app.models import Achievement


class AchievementAdmin(ModelView, model=Achievement):
    column_list = [
        Achievement.id,
        Achievement.name,
        Achievement.description,
        Achievement.profiles,
    ]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = 'Achievement'
    name_plural = 'Achievements'
    icon = 'fa-solid fa-medal'
    category = 'ACCOUNTS'
    column_searchable_list = [Achievement.name]
    column_sortable_list = [Achievement.id]
