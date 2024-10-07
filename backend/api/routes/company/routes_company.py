from aiohttp.web_request import Request
import aiohttp_sqlalchemy
from aiohttp import web

from api import middlewares
from api.routes.company.form import PositionForm
from api.routes.public.typing import RegistrationPayload
from pkg import response, utils
from pkg.app_keys import share_keys, AppKeys
from pkg.consts import Role
from pkg.models import User
from pkg.models.models import Company

# testing
from pkg.services.common.new_registrator import MemberRegistration, registration_process


def setup_company_routes(app: web.Application):
    company = web.Application()

    company["config"] = app["config"]
    share_keys(app, company)
    company.middlewares.append(middlewares.auth_middleware)
    company.middlewares.append(middlewares.roles_required([Role.COMPANY_MEMBER, Role.COMPANY_ADMIN]))

    company.router.add_post("/create-member", handle_create_member)
    company.router.add_post("/position", handle_create_position)
    company.router.add_get("/positions", handle_list_position)
    company.router.add_get("/position/{id}", handle_position)
    company.router.add_patch("/position/{id}", handle_patch_position)
    company.router.add_delete("/position/{id}", handle_delete_position)

    app.add_subapp("/api/company/", company)


async def handle_create_member(request: web.Request):
    session = aiohttp_sqlalchemy.get_session(request)
    payload = await utils.request_payload(request, RegistrationPayload)
    if payload.type != Role.COMPANY_MEMBER:
        return response.error_response(None, ["Only company members allowed"])

    user: User = request["user"]
    company: Company = request["company"]

    member: MemberRegistration = MemberRegistration(
        company_id=str(company.id),
        registrator_user_id=str(user.id),
        name=payload.name,
        email=payload.email,
        password=payload.password,
        password_confirm=payload.password_confirm,
    )
    user = await registration_process(
        type_=Role.COMPANY_MEMBER,
        data=member.model_dump(),
        publisher=request.app[AppKeys.service_events],
        session=session,
    )

    if not user:
        return response.error_response(None, ["User was not created"])

    return response.success_response(user.json(), [])

async def handle_create_position(request: web.Request):
    payload = await utils.request_payload(request, PositionForm)
    session = aiohttp_sqlalchemy.get_session(request)
    user: User = request["user"]
    company: Company = request["company"]
    payload.company_id = str(user.manager.company_id)
    service = request.app[AppKeys.service_position]
    position = await service.create_new_position(session, payload)


    return response.success_response(position.json(), [])


async def handle_list_position(request: web.Request):
    # async with request.app["session"] as session:
    #     positions = await repositories.get_positions(
    #         session, company_id=request["user"].manager.company_id
    #     )
    #
    # return response.success_response(
    #     {
    #         "positions": [p.json() for p in positions],
    #     },
    #     messages=[],
    # )
    return response.success_response({}, [])


async def handle_patch_position(request: web.Request):
    # id = UUID(request.match_info.get("id"), version=4)
    #
    # payload = await utils.request_payload(request, PositionFormPatch)
    #
    # # ???
    # if isinstance(payload, web.Response):
    #     return payload
    #
    # async with request.app["session"] as session:
    #     position = await repositories.update_position(session, id, payload)
    #     if not position:
    #         return response.error_response(None, messages=["unable to update position"])
    #
    # return response.success_response(position.json(), messages=[])
    return response.success_response({}, [])


async def handle_position(request: web.Request):
    # id = UUID(request.match_info.get("id"), version=4)
    #
    # async with request.app["session"] as session:
    #     position = await repositories.get_position(session, id=id)
    #     if not position:
    #         return response.error_response(
    #             None,
    #             messages=["Position with given id not found"],
    #             status=HTTPStatus.NOT_FOUND,
    #         )
    #
    # return response.success_response(position.json(), messages=[])
    #
    return response.success_response({}, [])


async def handle_delete_position(request: web.Request):
    # return response.error_response(
    #     None, messages=["Method not implemented"], status=HTTPStatus.NOT_IMPLEMENTED
    # )
    return response.success_response({}, [])
