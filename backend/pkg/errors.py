def create_form_error(field: str, msg: str):
    return {
        "type": "value_error",
        "loc": [field],
        "msg": msg,
    }
