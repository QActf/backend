from typing import Optional

from pydantic import BaseModel, Field


class TariffRead(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True


class TariffCreate(BaseModel):
    name: str
    description: Optional[str]


class TariffCreated(TariffCreate):
    id: int

    class Config:
        from_attributes = True


class TariffUpdate(BaseModel):
    name: Optional[str] = Field(None,)
    description: Optional[str] = Field(None,)
