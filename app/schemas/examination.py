from typing import Optional

from pydantic import BaseModel


class ExaminationCreate(BaseModel):
    name: str
    description: Optional[str]


class ExaminationRead(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True
