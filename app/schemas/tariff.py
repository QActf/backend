from typing import Optional

from pydantic import BaseModel, Field


class TariffRead(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True


class TariffCreate(BaseModel):
    name: str = Field(... , example="Название тарифа")
    description: Optional[str] = Field(... , example="Описание тарифа")


class TariffCreated(TariffCreate):
    id: int

    class Config:
        from_attributes = True


class TariffUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Название тарифа")
    description: Optional[str] = Field(None, example="Описание тарифа")
