from sqladmin import ModelView

from app.models import (
    Achievements, Auth, Common, Contacts, Errors, Header, Help, Locale, Main,
    Months, ProfileUser, QuestionBanner, Restore, Secure, Subscription, Tasks,
)


class LocaleAdmin(ModelView, model=Locale):
    column_list = [Locale.id, Locale.language]
    can_create = True
    can_edit = False
    can_delete = True
    can_view_details = True
    name = 'Locale'
    name_plural = 'Locales'
    icon = 'fa-solid fa-language'
    category = 'LANGUAGES'
    column_searchable_list = [Locale.language]


def admin_decor(cls):
    class _class(cls):
        column_list = [cls.model.id, cls.model.locale]
        icon = 'fa-solid fa-quote-right'
        can_create = False
        can_edit = True
        can_delete = False
        can_view_details = True
        category = 'LANGUAGES'
    return _class


@admin_decor
class CommonAdmin(ModelView, model=Common):
    name_plural = 'Common'


@admin_decor
class HeaderAdmin(ModelView, model=Header):
    name_plural = 'Headers'


@admin_decor
class AuthAdmin(ModelView, model=Auth):
    name_plural = 'Authentication'


@admin_decor
class ContactsAdmin(ModelView, model=Contacts):
    name_plural = 'Contacts'


@admin_decor
class HelpAdmin(ModelView, model=Help):
    name_plural = 'Help'


@admin_decor
class MainAdmin(ModelView, model=Main):
    name_plural = 'Main'


@admin_decor
class RestoreAdmin(ModelView, model=Restore):
    name_plural = 'Restore'


@admin_decor
class SubscriptionAdmin(ModelView, model=Subscription):
    name_plural = 'Subscriptions'


@admin_decor
class ProfileUserAdmin(ModelView, model=ProfileUser):
    name_plural = 'Profiles'


@admin_decor
class SecureAdmin(ModelView, model=Secure):
    name = 'Security'
    name_plural = 'Security'


@admin_decor
class AchievementsAdmin(ModelView, model=Achievements):
    name_plural = 'Achievements'


@admin_decor
class TasksAdmin(ModelView, model=Tasks):
    name_plural = 'Tasks'


@admin_decor
class QuestionBannerAdmin(ModelView, model=QuestionBanner):
    name = 'Question Banner'
    name_plural = 'Banners with questions'


@admin_decor
class ErrorsAdmin(ModelView, model=Errors):
    name_plural = 'Errors'


@admin_decor
class MonthsAdmin(ModelView, model=Months):
    name_plural = 'Months'
