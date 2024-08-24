from uuid import UUID
from pydantic import (
    BaseModel,
    field_validator,
    model_validator,
    EmailStr
)
from typing import Optional
from typing_extensions import Self
from globalTypes import RegistrationType


class RegistrationPayload(BaseModel, extra="forbid"):
    type: RegistrationType
    name: str
    email: EmailStr
    password: str
    password_confirm: str
    companyName: Optional[str] = None

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        pw1 = self.password
        pw2 = self.password_confirm
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
        return self


class ConfirmCodePayload(BaseModel):
    id: str
    code: str

    @field_validator('code')
    @classmethod
    def validate_code_length(cls, v):
        if len(str(v)) != 6:
            raise ValueError("Code should have exactly 6 characters")
        return v

    @field_validator('id')
    @classmethod
    def validate_id_uuid(cls, v):
        """This code will raise ValueException and pydantic catch this
        exception and show error about invalid UUID"""
        UUID(v, version=4)
        # othervice it will return data
        return v

    @model_validator(mode='before')
    @classmethod
    def no_additional_fields(cls, data):
        if len(data) > 2:
            raise ValueError("Too many arguments")
        return data


# Example usage:
#
# def main():
#     data = {
#         "id": "d1bd174c-)3d34-453b-b2e7-9bcbbeb67d40",
#         "code": "123123123",
#     }
#
#     try:
#         confirm_code = ConfirmCodePayload(**data)
#         print(confirm_code)
#
#     except ValidationError as err:
#         error_json = err.json()
#         print(error_json)
#
#
# if __name__ == "__main__":
#     main()
