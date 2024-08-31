import re
from pydantic import ValidationError
from sqlalchemy.exc import (
    DataError,
    IntegrityError,
    SQLAlchemyError,
)



def create_form_error(field: str, msg: str, err_type: str = "value_error"):
    return {
        "type": err_type,
        "loc": [field],
        "msg": msg,
    }

def validation_errors(err: ValidationError):
    return err.errors(include_url=False, include_input=False, include_context=False)


def parse_sqlalchemy_error(error: SQLAlchemyError):
    field = None
    error_type = None
    message = str(error)

    if isinstance(error, IntegrityError):
        error_type = "IntegrityError"
        if "UNIQUE constraint failed" in message or "duplicate key" in message:
            error_type = "UniqueViolation"

        elif "FOREIGN KEY constraint failed" in message or "foreign key" in message:
            error_type = "ForeignKeyViolation"

        elif "NotNullViolationError" in message:
            error_type = "NotNullViolationError"

    elif isinstance(error, DataError):
        error_type = "DataError"

        if "value too long" in message or "data too long" in message:
            error_type = "ValueTooLong"

        elif "invalid input syntax" in message or "incorrect" in message:
            error_type = "InvalidInputSyntax"

    # get field or key
    match = re.search(r'column\s"(\w+)"', message)
    if match:
        field = match.group(1)

    match = re.search(r'unique constraint \"(\w+)\"', message)
    if match:
        field = match.group(1).replace("_key", "")

    match = re.search(r'Key \((\w+)\)=\((.+?)\)', message)
    if match:
        field = match.group(1)

    return create_form_error(str(field), f"{error_type} on {field} field", str(error_type))

