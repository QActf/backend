from typing import Optional

from pydantic import BaseModel, Field


class ExaminationCreate(BaseModel):
    name: str
    description: Optional[str]


class ExaminationRead(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True


class ExaminationUpdate(BaseModel):
    name: Optional[str] = Field(None,)
    description: Optional[str] = Field(None,)
