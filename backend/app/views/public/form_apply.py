from http import HTTPStatus
from aiohttp import web


def setup_apply_routes(app: web.Application):
    app.router.add_post('/api/apply/form', apply_form)
    app.router.add_get('/api/apply/result', get_result)


async def apply_form(request: web.Request) -> web.Response:
    data = await request.json()
    if not data:
        return web.json_response({
            "data": "",
            "message": "Payload was not provided",
            "success": True,
        }, status=HTTPStatus.BAD_REQUEST)

    return web.json_response({
        "data": data,
        "message": "Your request was successfully applied",
        "success": True,
    }, status=HTTPStatus.OK)


async def get_result(request: web.Request) -> web.Response:
    if "id" not in request.rel_url.query:
        return web.json_response({
            "data": "",
            "message": "Your submition id was not provided",
            "success": True,
        }, status=HTTPStatus.BAD_REQUEST)

    id = int(request.rel_url.query['id'])
    return web.json_response({
        "data": id,
        "message": "Your results",
        "success": True,
    }, status=HTTPStatus.OK)
