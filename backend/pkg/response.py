from http import HTTPStatus
from typing import Any, List, Union

from aiohttp import web
from pydantic import BaseModel


class ResponseData(BaseModel):
    data: Any
    messages: Union[List[str], None]
    errors: Any
    status: bool


def success_response(payload: Any, messages: List[str]) -> web.Response:
    response = ResponseData(data=payload, messages=messages, errors=[], status=True)
    return web.json_response(response.model_dump(), status=HTTPStatus.OK)


def error_response(
    errors: Any, messages: List[str], status: HTTPStatus = HTTPStatus.BAD_REQUEST
) -> web.Response:
    response = ResponseData(data=None, messages=messages, errors=errors, status=False)
    return web.json_response(response.model_dump(), status=status)
