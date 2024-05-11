from http import HTTPStatus
from aiohttp import web
from pydantic import ValidationError

from app.models import AdminCreateUserPayload
from app.repositories import users


def setup_admin_routes(app: web.Application):
    app.router.add_post('/api/admin/create-user', create_user)


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
        return web.json_response({"errors": error_messages},
                                 status=HTTPStatus.BAD_REQUEST)

    async with request.app['db'].acquire() as conn:
        result = users.UserRepository(conn).create(payload)
    return web.json_response({"status": result})
