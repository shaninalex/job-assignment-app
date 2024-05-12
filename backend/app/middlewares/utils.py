import time
from aiohttp import web

from app.settings import TIMEOUT


@web.middleware
async def timeout_middleware(request, handler):
    # sinse this is just example backend, current middleware simulate
    # slow request process. You can enable/disable this with settings
    if TIMEOUT:
        time.sleep(2)
    return await handler(request)


async def handle_404(request):
    return web.json_response({'error': 404}, status=404)


async def handle_500(request):
    return web.json_response({'error': 500}, status=500)


def create_error_middleware(overrides):

    @web.middleware
    async def error_middleware(request, handler):
        try:
            return await handler(request)
        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request)

            raise
        except Exception:
            request.protocol.logger.exception("Error handling request")
            return await overrides[500](request)

    return error_middleware


def setup_middlewares(app):
    error_middleware = create_error_middleware({
        404: handle_404,
        500: handle_500
    })
    app.middlewares.append(timeout_middleware)
    app.middlewares.append(error_middleware)
