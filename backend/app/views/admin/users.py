from http import HTTPStatus

from aiohttp import web


def setup_user_routes(app: web.Application):
    app.router.add_get('/user/me', get_current_user)


async def get_current_user(request):
    return web.json_response({
        "data": request["user"].json(),
        "message": "",
        "success": True,
    })

