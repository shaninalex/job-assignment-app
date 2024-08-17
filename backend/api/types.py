from marshmallow import Schema, fields, validates_schema, ValidationError
from globalTypes import RegistrationType


class RegisterPayload(Schema):
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
            errors["password_confirm"] = ["password confirm should be equal to password"]
            raise ValidationError(errors)

        if "name" not in data and data["type"] == RegistrationType.CANDIDATE:
            errors["name"] = ["User name is required"]
            raise ValidationError(errors)

        if data["type"] == RegistrationType.COMPANY:
            if "companyName" not in data:
                errors["companyName"] = ["Company name is required"]
            if "name" not in data:
                errors["name"] = ["Company admin name is required"]
            raise ValidationError(errors)