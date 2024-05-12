from http import HTTPStatus
from aiohttp import web
from pydantic import ValidationError

from app.db import Role
from app.models import AdminCreateUserPayload
from app.repositories import users


def setup_admin_routes(app: web.Application):
    app.router.add_post('/create-user', create_user)


async def create_user(request):
    if request["user"].role is not Role.admin:
        return web.json_response({
            "data": {
                "error": "You have not enough permissions",
            },
            "message": "Request forbidden",
            "success": False,
        }, status=HTTPStatus.FORBIDDEN)

    data = await request.json()
    try:
        payload: AdminCreateUserPayload = AdminCreateUserPayload(**data)

        async with request.app['db'].acquire() as conn:
            try:
                result = await users.create(conn, payload)
                return web.json_response({
                    "data": result.to_json(),
                    "message": "user was added",
                    "success": True,
                }, status=HTTPStatus.CREATED)

            except Exception as e:
                return web.json_response({
                    "data": {
                        "error": str(e),
                    },
                    "message": "There some error happend",
                    "success": False,
                }, status=HTTPStatus.BAD_REQUEST)

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
            "message": "There some errors",
            "success": False,
        }, status=HTTPStatus.BAD_REQUEST)


