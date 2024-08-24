from uuid import UUID
from pydantic import BaseModel, ValidationError, field_validator, model_validator


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
        UUID(v, version=4)

    @model_validator(mode='before')
    @classmethod
    def no_additional_fields(cls, data):
        if len(data) > 2:
            raise ValueError("Too many arguments")
        return data


def main():
    data = {
        "id": "d1bd174c-)3d34-453b-b2e7-9bcbbeb67d40",
        "code": "123123123",
    }

    try:
        confirm_code = ConfirmCodePayload(**data)
        print(confirm_code)

    except ValidationError as err:
        error_json = err.json()
        print(error_json)


if __name__ == "__main__":
    main()
