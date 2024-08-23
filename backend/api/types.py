"""
TODO: move forms into separate file since this is only for types
"""

from typing import TypedDict, Optional
from marshmallow import Schema, fields, validates_schema, ValidationError, validate
from globalTypes import RegistrationType


class RegisterForm(Schema):
    name = fields.Str()
    companyName = fields.Str()
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    password_confirm = fields.Str(required=True)
    type = fields.Enum(RegistrationType, required=True)

    @validates_schema
    def password_equal(self, data, **kwargs):
        errors = {}
        if data["password"] != data["password_confirm"]:
            errors["password_confirm"] = [
                "password confirm should be equal to password"
            ]
            raise ValidationError(errors)

        if data["type"] == RegistrationType.CANDIDATE:
            if "name" not in data:
                errors["name"] = ["User name is required"]
            raise ValidationError(errors)

        if data["type"] == RegistrationType.COMPANY:
            if "companyName" not in data:
                errors["companyName"] = ["Company name is required"]
            if "name" not in data:
                errors["name"] = ["Company admin name is required"]
            raise ValidationError(errors)


class RegistrationPayload(TypedDict):
    name: str
    companyName: Optional[str]
    age: str
    email: str
    password: str
    type: RegistrationType


class ConfirmCodePayload(TypedDict):
    id: str
    email: str


class ConfirmCodeForm(Schema):
    id = fields.Str(required=True)
    code = fields.Str(required=True, validate=[validate.Length(max=6, min=6)])