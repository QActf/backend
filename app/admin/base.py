from app.admin import (
    AchievementAdmin, CourseAdmin, ExaminationAdmin, GroupAdmin, ProfileAdmin,
    TariffAdmin, TaskAdmin, UserAdmin,
)

admin_models = [
    # category = 'accounts'
    GroupAdmin,
    UserAdmin,
    ProfileAdmin,
    AchievementAdmin,

    # category = 'Tariff'
    TariffAdmin,

    # category = 'training'
    CourseAdmin,
    TaskAdmin,
    ExaminationAdmin,
]


async def add_admin_models(admin):
    for admin_model in admin_models:
        admin.add_view(admin_model)
