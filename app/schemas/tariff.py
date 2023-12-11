from pydantic import BaseModel


class TariffRead(BaseModel):
    name: str
    description: str


class TariffCreate(TariffRead):
    pass
