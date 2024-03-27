from typing import Optional

from pydantic import BaseModel, Field


class ExaminationCreate(BaseModel):
    name: str = Field(..., example="Название экзамена")
    description: Optional[str] = Field(..., example="Описание экзамена")


class ExaminationRead(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True


class ExaminationUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Название экзамена")
    description: Optional[str] = Field(None, example="Название экзамена")
