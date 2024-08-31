import json
from http import HTTPStatus
from uuid import UUID
from aiohttp import web
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from database import repositories
from api import middlewares
from globalTypes import Role
from .types import PositionForm, PositionFormPatch


def setup_company_routes(app: web.Application):
    admin = web.Application()

    admin["session"] = app["session"]
    admin["mq"] = app["mq"]

    admin.middlewares.append(middlewares.auth_middleware)
    admin.middlewares.append(middlewares.roles_required([Role.COMPANY_MANAGER, Role.COMPANY_ADMIN]))

    admin.router.add_post("/position", handle_create_position)
    admin.router.add_get("/positions", handle_list_position)
    admin.router.add_get("/position/{id}", handle_position)
    admin.router.add_patch("/position/{id}", handle_patch_position)
    admin.router.add_delete("/position/{id}", handle_delete_position)

    app.add_subapp('/api/company/', admin)


async def handle_create_position(request: web.Request):
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
            payload.company_id = request["user"].manager.company_id
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
    async with request.app["session"] as session:
        positions = await repositories.get_positions(session, company_id=request["user"].manager.company_id) 
    return web.json_response({
        "positions": [p.json() for p in positions],
    }, status=HTTPStatus.OK)


async def handle_patch_position(request: web.Request):
    id = UUID(request.match_info.get("id"), version=4)

    data = await request.json()
    try:
        payload = PositionFormPatch(**data)
    except ValidationError as err:
        return web.json_response(
            json.loads(
                err.json(include_url=False, include_input=False,
                         include_context=False)
            ),
            status=HTTPStatus.BAD_REQUEST,
        )

    async with request.app["session"] as session:
        position = await repositories.update_position(session, id, payload)
        if not position:
            return web.json_response({"error": "unable to update position"}, status=HTTPStatus.BAD_REQUEST)
    return web.json_response(position.json(), status=HTTPStatus.OK)


async def handle_position(request: web.Request):
    id = UUID(request.match_info.get("id"), version=4)

    async with request.app["session"] as session:
        position = await repositories.get_position(session, id=id)
        if not position:
            return web.json_response({"error": "unable to get position"}, status=HTTPStatus.BAD_REQUEST)
    return web.json_response(position.json(), status=HTTPStatus.OK)


async def handle_delete_position(request: web.Request):
    return web.json_response(request["user"].json(), status=HTTPStatus.OK)
