from pydantic import BaseModel, EmailStr, Field


class ContactInformationBlockCreate(BaseModel):
    phones: list[str]
    email: EmailStr


class ContactInformationBlockRead(BaseModel):
    phones: list[str] | None
    email: EmailStr | None

    class Config:
        from_attributes = True


class ContactInformationBlockUpdate(ContactInformationBlockRead):
    phones: list[str] | None = Field(None)
    email: EmailStr | None = Field(None)
