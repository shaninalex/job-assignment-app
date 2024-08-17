from http import HTTPStatus
from aiohttp import web
from database import Staff
from uuid import uuid4

def setup_auth_routes(app: web.Application):
    app.router.add_post("/api/auth/login", login_user)


async def login_user(request: web.Request) -> web.Response:
    data = await request.json()
    data["password"] = str(uuid4())

    async with request.app["session"] as session:
        staff = Staff(**data)
        session.add(staff)
        await session.commit()
        return web.json_response({"data": staff.json()}, status=HTTPStatus.OK)
