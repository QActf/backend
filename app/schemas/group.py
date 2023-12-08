from pydantic import BaseModel


class GroupRead(BaseModel):
    name: str
    description: str


class GroupCreate(GroupRead):
    pass
