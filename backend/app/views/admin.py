from http import HTTPStatus
from aiohttp import web
from pydantic import ValidationError

from app.models import AdminCreateUserPayload
from app.repositories import users


def setup_admin_routes(app: web.Application):
    app.router.add_post('/create-user', create_user)


async def create_user(request):
    data = await request.json()  # form data
    try:
        payload: AdminCreateUserPayload = AdminCreateUserPayload(**data)
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

    async with request.app['db'].acquire() as conn:
        result = await users.create(conn, payload)
    return web.json_response({
        "data": result,
        "message": "User was added",
        "success": False,
    }, status=201)
