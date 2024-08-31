from http import HTTPStatus
import random
from typing import Type, TypeVar, Union

from aiohttp import web
from pydantic import BaseModel, ValidationError

from pkg import errors, response


def generate_code(length: int):
    if length <= 0:
        length = 6
    lower_bound = 10 ** (length - 1)
    upper_bound = 10**length - 1
    return f"{random.randint(lower_bound, upper_bound)}"


T = TypeVar('T', bound=BaseModel)

async def request_payload(request: web.Request, model_class: Type[T]) -> Union[web.Response, T]:
    try:
        data = await request.json()
    except ValueError:
        return response.error_response(None, messages=["Invalid payload"])

    if not data.keys():
        return response.error_response(None, messages=["Payload is empty"])

    try:
        payload = model_class(**data)
    except ValidationError as err:
        return response.error_response(errors.validation_errors(err))
    
    return payload

