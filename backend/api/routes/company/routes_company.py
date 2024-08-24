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

    app.add_subapp('/api/company/', admin)


# TODO: role COMPANY_*** required
async def handle_create_position(request: web.Request):
    return web.json_response(request["user"].json(), status=HTTPStatus.OK)
