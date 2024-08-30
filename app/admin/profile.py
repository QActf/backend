from sqladmin import ModelView

from app.models import Profile


class ProfileAdmin(ModelView, model=Profile):
    column_exclude_list = [Profile.image, Profile.user_id]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = 'Profile'
    name_plural = 'Profiles'
    icon = 'fa-regular fa-address-card'
    category = 'ACCOUNTS'
    column_searchable_list = [Profile.user]
    column_sortable_list = [Profile.id, Profile.birthday]
