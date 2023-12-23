from sqladmin import ModelView

from app.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.role, User.email]
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    category = "accounts"
    column_searchable_list = [User.username]
    column_sortable_list = [User.id]
    column_formatters = {User.username: lambda m, a: m.username[:10]}
