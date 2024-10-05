import random
from typing import Type, TypeVar

from aiohttp import web
from pydantic import BaseModel


def generate_code(length: int):
    if length <= 0:
        length = 6
    lower_bound = 10 ** (length - 1)
    upper_bound = 10**length - 1
    return f"{random.randint(lower_bound, upper_bound)}"


T = TypeVar("T", bound=BaseModel)


async def request_payload(request: web.Request, model_class: Type[T]) -> T:
    data = await request.json()
    if not data.keys():
        raise ValueError("Payload is empty")
    payload = model_class(**data)
    return payload
