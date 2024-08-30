from pydantic import BaseModel

from app.schemas.tariff import TariffPlanRead


class SubscriptionCreate(BaseModel):
    user_id: int
    tariff_id: int


class PlanRead(BaseModel):
    courses: list[dict]
    tariffs: list[TariffPlanRead]
