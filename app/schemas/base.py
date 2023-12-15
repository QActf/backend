from pydantic import BaseModel


class BaseRead(BaseModel):
    name: str
    description: str


class BaseCreate(BaseRead):
    pass
