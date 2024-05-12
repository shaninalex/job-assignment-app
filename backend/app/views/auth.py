from http import HTTPStatus
from aiohttp import web
from pydantic import ValidationError
from app.repositories import auth

from app.models import LoginPayload


def setup_auth_routes(app: web.Application):
    app.router.add_post('/api/auth/login', login_user)


async def login_user(request: web.Request) -> web.Response:
    data = await request.json()  # form data
    try:
        payload: LoginPayload = LoginPayload(**data)
        async with request.app['db'].acquire() as conn:
            response = await auth.login(conn, payload)
            if response:
                return web.json_response({
                    "data": response.model_dump(),
                    "message": "successfully authenticated",
                    "success": True,
                }, status=HTTPStatus.OK)
            return web.json_response({"errors": "creadentials are incorrect"}, status=HTTPStatus.BAD_REQUEST)
    except ValidationError as e:
        errors = e.errors()
        error_messages = []
        for error in errors:
            error_messages.append({
                "field": error["loc"][0],
                "error_message": error["msg"]
            })
        return web.json_response({
            "data": error_messages,
            "message": "There are some authentication errors",
            "success": False,
        }, status=HTTPStatus.BAD_REQUEST)

