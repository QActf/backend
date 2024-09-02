from app.admin import (
    AchievementAdmin, AchievementsAdmin, AuthAdmin, CommonAdmin, ContactsAdmin,
    CourseAdmin, ErrorsAdmin, ExaminationAdmin, GroupAdmin, HeaderAdmin,
    HelpAdmin, LocaleAdmin, MainAdmin, MonthsAdmin, ProfileAdmin,
    ProfileUserAdmin, QuestionAdmin, QuestionBannerAdmin, RestoreAdmin,
    SecureAdmin, SubscriptionAdmin, TariffAdmin, TaskAdmin, TasksAdmin,
    UserAdmin,
)

admin_models = [
    # category = 'ACCOUNTS'
    GroupAdmin, UserAdmin, ProfileAdmin, AchievementAdmin,

    # category = 'TARIFF'
    TariffAdmin,

    # category = 'TRAINING'
    CourseAdmin, TaskAdmin, ExaminationAdmin,

    # category = 'LANGUAGES'
    LocaleAdmin, CommonAdmin, HeaderAdmin, AuthAdmin, ContactsAdmin,
    HelpAdmin, MainAdmin, RestoreAdmin, SubscriptionAdmin,
    ProfileUserAdmin, SecureAdmin, AchievementsAdmin, TasksAdmin,
    QuestionBannerAdmin, ErrorsAdmin, MonthsAdmin,

    # category = 'HELP'
    QuestionAdmin,
]


async def add_admin_models(admin):
    for admin_model in admin_models:
        admin.add_view(admin_model)
