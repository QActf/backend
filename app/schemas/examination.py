from pydantic import BaseModel


class ExaminationRead(BaseModel):
    name: str
    description: str


class ExaminationCreate(ExaminationRead):
    pass
