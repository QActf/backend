from app.admin import TariffAdmin, UserAdmin

admin_models = [
    UserAdmin,
    TariffAdmin,
]


async def add_admin_models(admin):
    for admin_model in admin_models:
        admin.add_view(admin_model)
