from aiohttp import web

def setup_auth_routes(app: web.Application):
    app.router.add_post('/api/auth/login', login_user)
    app.router.add_post('/api/auth/refresh', refresh_token)


async def login_user(request):
    return web.json_response({"token": "jwt token string"})

async def refresh_token(request):
    return web.json_response({"token": "refreshed jwt"})