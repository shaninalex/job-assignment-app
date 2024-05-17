from http import HTTPStatus

from aiohttp import web


def setup_apply_routes(app: web.Application):
    app.router.add_post('/api/apply/form', apply_form)
    app.router.add_get('/api/apply/result', get_result)


async def apply_form(request: web.Request) -> web.Response:
    # data: ApplyPayload = await request.json()
    # try:
    #     async with request.app['db'].acquire() as conn:
    #         payload: ApplyPayload = ApplyPayload(**data)
    #         try:
    #             await candidates.save(conn, payload)
    #             return web.json_response({
    #                 "data": None,
    #                 "message": "Your request was successfully applied",
    #                 "success": True,
    #             }, status=HTTPStatus.OK)
    #         except Exception as e:
    #             return web.json_response({
    #                 "data": {"errors": str(e)},
    #                 "message": "There some errors",
    #                 "success": False,
    #             }, status=HTTPStatus.BAD_REQUEST)
    #
    # except ValidationError as e:
    #     error_messages = validation_error(e)
    #     return web.json_response({
    #         "data": error_messages,
    #         "message": "There some errors",
    #         "success": False,
    #     }, status=HTTPStatus.BAD_REQUEST)
    return web.json_response({
        "data": None,
        "message": "Not implemented yet",
        "success": False,
    }, status=HTTPStatus.BAD_REQUEST)


async def get_result(request: web.Request) -> web.Response:
    # if "id" not in request.rel_url.query:
    #     return web.json_response({
    #         "data": "",
    #         "message": "Your submition id was not provided",
    #         "success": True,
    #     }, status=HTTPStatus.BAD_REQUEST)
    #
    # id = int(request.rel_url.query['id'])
    # return web.json_response({
    #     "data": id,
    #     "message": "Your results",
    #     "success": True,
    # }, status=HTTPStatus.OK)
    return web.json_response({
        "data": None,
        "message": "Not implemented yet",
        "success": False,
    }, status=HTTPStatus.BAD_REQUEST)
