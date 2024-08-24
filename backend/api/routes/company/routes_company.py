from http import HTTPStatus
from aiohttp import web
from api import middlewares
from globalTypes import Role


def setup_company_routes(app: web.Application):
    admin = web.Application()

    admin["session"] = app["session"]
    admin["mq"] = app["mq"]

    admin.middlewares.append(middlewares.auth_middleware)
    admin.middlewares.append(middlewares.roles_required([Role.COMPANY_MANAGER, Role.COMPANY_ADMIN]))

    admin.router.add_post("/position", handle_create_position)
    admin.router.add_get("/position", handle_list_position)
    admin.router.add_patch("/position", handle_patch_position)
    admin.router.add_delete("/position", handle_delete_position)

    app.add_subapp('/api/company/', admin)


async def handle_create_position(request: web.Request):
    return web.json_response(request["user"].json(), status=HTTPStatus.OK)

async def handle_list_position(request: web.Request):
    return web.json_response(request["user"].json(), status=HTTPStatus.OK)

async def handle_patch_position(request: web.Request):
    return web.json_response(request["user"].json(), status=HTTPStatus.OK)

async def handle_delete_position(request: web.Request):
    return web.json_response(request["user"].json(), status=HTTPStatus.OK)
