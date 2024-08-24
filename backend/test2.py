from typing_extensions import Self
from pydantic import BaseModel, ValidationError, field_validator, model_validator, EmailStr
from globalTypes import RegistrationType
from typing import Optional


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


def main():
    data = {
        "type": "company",
        "name": "Barry",
        "email": "test@test.com",
        "password": "password",
        "password_confirm": "password",
        "companyName": "hello COmpany"
    }

    try:
        confirm_code = RegistrationPayload(**data)
        print(confirm_code)

    except ValidationError as err:
        error_json = err.json(indent=4, include_url=False, include_input=False)
        print(error_json)


if __name__ == "__main__":
    main()
