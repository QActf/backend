from typing import Optional

from pydantic import BaseModel


class TariffRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    users: Optional[list[int]]

    class Config:
        from_attributes = True


class TarifCreate(BaseModel):
    name: str
    description: Optional[str]


class TariffCreated(TarifCreate):
    id: int

    class Config:
        from_attributes = True
