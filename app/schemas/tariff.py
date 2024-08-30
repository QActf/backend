from typing import Optional

from pydantic import BaseModel, Field


class TariffRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    cost: int

    class Config:
        from_attributes = True


class TariffCreate(BaseModel):
    name: str
    description: Optional[str]
    cost: int


class TariffCreated(TariffCreate):
    id: int

    class Config:
        from_attributes = True


class TariffUpdate(BaseModel):
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    cost: int = Field(None)


class TariffPlanRead(TariffRead):
    dataIndex: str
    key: str
    is_active: bool
    this_tariff: bool
