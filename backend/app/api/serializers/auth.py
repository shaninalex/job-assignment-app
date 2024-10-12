from typing import Self
from pydantic import BaseModel, EmailStr, model_validator

from app.utilites.password import is_password_valid


class APIRegisterCandidatePayload(BaseModel, extra="forbid"):
    name: str
    email: EmailStr
    password: str
    password_confirm: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if not is_password_valid(self.password, self.password_confirm):
            raise ValueError("passwords do not match")
        return self


class APICreateCompanyPayload(BaseModel, extra="forbid"):
    name: str
    website: str  # pydantic.HttpUrl ?
    email: EmailStr
    company_admin_name: str
    company_admin_email: EmailStr
    password: str
    password_confirm: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if not is_password_valid(self.password, self.password_confirm):
            raise ValueError("passwords do not match")
        return self


class APILoginPayload(BaseModel, extra="forbid"):
    email: EmailStr
    password: str
