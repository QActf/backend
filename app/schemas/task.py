from pydantic import BaseModel


class TaskRead(BaseModel):
    name: str
    description: str


class TaskCreate(TaskRead):
    pass
