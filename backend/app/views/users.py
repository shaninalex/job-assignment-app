from aiohttp import web


def setup_user_routes(app: web.Application):
    app.router.add_post('/api/user/me', get_current_user)


async def get_current_user(request):
    return web.json_response({"current": "user"})
