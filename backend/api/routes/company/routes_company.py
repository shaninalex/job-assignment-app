import json
from http import HTTPStatus
from uuid import UUID
from aiohttp import web
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from database import repositories
from api import middlewares
from globalTypes import Role
from pkg import errors, response, utils
from .types import PositionForm, PositionFormPatch


def setup_company_routes(app: web.Application):
    company = web.Application()

    company["session"] = app["session"]
    company["mq"] = app["mq"]

    company.middlewares.append(middlewares.auth_middleware)
    company.middlewares.append(middlewares.roles_required([Role.COMPANY_MANAGER, Role.COMPANY_ADMIN]))

    company.router.add_post("/position", handle_create_position)
    company.router.add_get("/positions", handle_list_position)
    company.router.add_get("/position/{id}", handle_position)
    company.router.add_patch("/position/{id}", handle_patch_position)
    company.router.add_delete("/position/{id}", handle_delete_position)

    app.add_subapp('/api/company/', company)


async def handle_create_position(request: web.Request):
    payload = await utils.request_payload(request, PositionForm)
    if isinstance(payload, web.Response):
        return payload

    async with request.app["session"] as session:
        try:
            payload.company_id = request["user"].manager.company_id
            position = await repositories.create_position(session, payload)
            if position:
                return response.success_response(position.json())

            return response.error_response(None, ["unable to create position"])

        except SQLAlchemyError as e:
            await session.rollback()
            errs = errors.parse_sqlalchemy_error(e)
            return response.error_response(errs)


async def handle_list_position(request: web.Request):
    async with request.app["session"] as session:
        positions = await repositories.get_positions(session, company_id=request["user"].manager.company_id) 

    return response.success_response({
        "positions": [p.json() for p in positions],
    })


async def handle_patch_position(request: web.Request):
    id = UUID(request.match_info.get("id"), version=4)

    payload = await utils.request_payload(request, PositionFormPatch)
    if isinstance(payload, web.Response):
        return payload

    async with request.app["session"] as session:
        position = await repositories.update_position(session, id, payload)
        if not position:
            return response.error_response(None, ["unable to update position"])

    return response.success_response(position.json())


async def handle_position(request: web.Request):
    id = UUID(request.match_info.get("id"), version=4)

    async with request.app["session"] as session:
        position = await repositories.get_position(session, id=id)
        if not position:
            return response.error_response(None, ["Position with given id not found"], status=HTTPStatus.NOT_FOUND)

    return response.success_response(position.json())

async def handle_delete_position(request: web.Request):
    return response.error_response(None, ["Method not implemented"], status=HTTPStatus.NOT_IMPLEMENTED)

