from sqladmin import ModelView

from app.models import Group


class GroupAdmin(ModelView, model=Group):
    column_list = [Group.id, Group.name, Group.description]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = 'Group'
    name_plural = 'Groups'
    icon = 'fa-solid fa-user-group'
    category = 'ACCOUNTS'
    column_searchable_list = [Group.name]
    column_sortable_list = [Group.id]
