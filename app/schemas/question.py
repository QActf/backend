from typing import Optional

from pydantic import BaseModel


class QuestionRead(BaseModel):
    id: int
    problem: Optional[str]
    solution: Optional[str]

    class Config:
        from_attributes = True
