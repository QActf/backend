from pydantic import BaseModel


class ProfileRead(BaseModel):
    first_name: str
    second_name: str
    age: int


class ProfileCreate(ProfileRead):
    first_name: str
    second_name: str
    age: int
    user_id: int
