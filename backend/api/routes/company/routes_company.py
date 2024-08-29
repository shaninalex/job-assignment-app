import json
from http import HTTPStatus
from aiohttp import web
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from database import repositories
from api import middlewares
from globalTypes import Role
from .types import PositionForm


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
    print(request["user"].company_member.company)
    data = await request.json()
    try:
        payload = PositionForm(**data)
    except ValidationError as err:
        return web.json_response(
            json.loads(
                err.json(include_url=False, include_input=False,
                         include_context=False)
            ),
            status=HTTPStatus.BAD_REQUEST,
        )

    async with request.app["session"] as session:
        try:
            position = await repositories.create_position(session, payload)
            if position:
                return web.json_response(position.json(), status=HTTPStatus.OK)

            return web.json_response({"errors": ["unable to create position"]}, status=HTTPStatus.OK)

        except SQLAlchemyError as e:
            await session.rollback()
            return web.json_response(
                {"errors": [str(e)]}, status=HTTPStatus.BAD_REQUEST
            )


async def handle_list_position(request: web.Request):
    return web.json_response({
        "user": request["user"].json(),
        "manager": request["user"].manager.json(),
        "company": request["company"].json(),
        "company_managers": [m.json() for m in request["company"].managers],
    }, status=HTTPStatus.OK)

async def handle_patch_position(request: web.Request):
    return web.json_response(request["user"].json(), status=HTTPStatus.OK)

async def handle_delete_position(request: web.Request):
    return web.json_response(request["user"].json(), status=HTTPStatus.OK)
