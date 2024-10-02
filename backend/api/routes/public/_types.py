from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator, model_validator, EmailStr
from typing_extensions import Self

from pkg.consts import RegistrationType


class RegistrationPayload(BaseModel, extra="forbid"):
    type: RegistrationType
    name: str
    email: EmailStr
    password: str
    password_confirm: str
    company_name: Optional[str] = None

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        pw1 = self.password
        pw2 = self.password_confirm
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("passwords do not match")
        return self

    @model_validator(mode="after")
    def validate_company_fields(self) -> Self:
        if self.type == RegistrationType.COMPANY:
            if not self.company_name or len(self.company_name.strip()) == 0:
                raise ValueError("Company name is required for Company registration")
        return self

    @field_validator("company_name")
    @classmethod
    def validate_company_name(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError("Company name should not be empty")
        return v


class ConfirmCodePayload(BaseModel, extra="forbid"):
    id: str
    code: str

    @field_validator("code")
    @classmethod
    def validate_code_length(cls, v):
        if len(str(v)) != 6:
            raise ValueError("Code should have exactly 6 characters")
        return v

    @field_validator("id")
    @classmethod
    def validate_id_uuid(cls, v):
        # This code will raise ValueException if string is not UUID
        # and pydantic catch this
        # exception and show error about invalid UUID
        UUID(v, version=4)
        # otherwise it will return data
        return v


class LoginPayload(BaseModel, extra="forbid"):
    email: EmailStr
    password: str
