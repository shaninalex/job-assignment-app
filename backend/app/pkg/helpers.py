from pydantic import ValidationError
from typing import List


def validation_error(e: ValidationError) -> List[dict]:
    errors = e.errors()
    error_messages = []
    for error in errors:
        error_messages.append({
            "field": error["loc"][0],
            "error_message": error["msg"]
        })

    return error_messages
