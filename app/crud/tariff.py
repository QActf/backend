from app.crud.base import CRUDBase
from app.models import Tariff


class CRUDTariff(CRUDBase):
    pass


tariff_crud = CRUDTariff(Tariff)
