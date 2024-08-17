from http import HTTPStatus
from aiohttp import web
from database import Staff

def setup_auth_routes(app: web.Application):
    app.router.add_get("/api/auth/login", login_user)


async def login_user(request: web.Request) -> web.Response:
    async with request.app["session"]() as session:
        session.add_all(    
            [
                Staff(name="tes2t", email="test2@test.com", password="32asdasd9847324"),
            ]
        )
        await session.commit()
        return web.json_response({"data": "example"}, status=HTTPStatus.OK)
