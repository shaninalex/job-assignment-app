from http import HTTPStatus

from aiohttp import web


async def handle_app_health(request: web.Request):
    return web.json_response({"status": True, "version": "v0.6.1"}, status=HTTPStatus.OK)


def setup_utils_routes(app: web.Application):
    app.router.add_get("/health", handle_app_health)
