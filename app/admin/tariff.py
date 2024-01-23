from sqladmin import ModelView

from app.models import Tariff


class TariffAdmin(ModelView, model=Tariff):
    column_list = [Tariff.id, Tariff.name, Tariff.users]
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    name = "Tariff"
    name_plural = "Tariffs"
    icon = "fa-solid fa-dollar-sign"
    category = "tariff"
