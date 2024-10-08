import logging
import sys
import uuid
import aiohttp_sqlalchemy

from http import HTTPStatus
from typing import List
from aiohttp import web
from pydantic import BaseModel, EmailStr
from sqlalchemy import delete, select, update
from api import middlewares
from api.routes.company.form import PositionForm, PositionFormPatch
from pkg import password, utils, response
from pkg.app_keys import share_keys, AppKeys
from pkg.common import operations
from pkg.consts import AuthStatus, ConfirmStatusCode, Role
from pkg.models.models import CompanyManager, ConfirmCode, User, Position, Company
from pkg.services.event_service import Exchanges, RoutingKeys


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


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


class MemberRegistration(BaseModel, extra="forbid"):
    company_id: str
    registrator_user_id: str  # id of a user who add this member
    name: str
    email: EmailStr
    role: Role
    password: str
    password_confirm: str


async def handle_create_member(request: web.Request):
    session = aiohttp_sqlalchemy.get_session(request)
    payload = await utils.request_payload(request, MemberRegistration)
    if payload.role != Role.COMPANY_MEMBER or payload.role != Role.COMPANY_ADMIN:
        return response.error_response(None, ["Only company members allowed"])

    if operations.is_user_exists(session, payload.email):
        return response.error_response(None, ["User already exists"])

    user: User = request["user"]
    company: Company = request["company"]
    user = User(
        id=uuid.uuid4(),
        email=payload.email,
        name=payload.name,
        role=payload.role,
        status=AuthStatus.PENDING,
        password_hash=password.get_hashed_password(payload.password),
        codes=[
            ConfirmCode(
                code=utils.generate_code(6),
                # The status should be:
                # status=ConfirmStatusCode.CREATED
                # But since we do not implement email service yet
                # we will assume that confirm status is already sent
                status=ConfirmStatusCode.SENT,
            )
        ],
        manager=CompanyManager(company=company),
    )
    session.add(user)
    await session.flush()
    await session.refresh(user)

    await request.app[AppKeys.service_events].publish_event(
        Exchanges.ADMIN, RoutingKeys.NEW_COMPANY_MEMBER, {"user": user.json()}
    )
    await request.app[AppKeys.service_events].publish_event(
        Exchanges.EMAIL, RoutingKeys.NEW_COMPANY_MEMBER, {"user": user.json()}
    )
    return response.success_response(user.json(), [])


async def handle_create_position(request: web.Request):
    payload = await utils.request_payload(request, PositionForm)
    session = aiohttp_sqlalchemy.get_session(request)
    user: User = request["user"]
    payload.company_id = str(user.manager.company_id)
    position = await operations.create_new_position(session, payload)
    await request.app[AppKeys.service_events].publish_event(Exchanges.ADMIN, RoutingKeys.NEW_POSITION, {"position": position.json()})
    return response.success_response(position.json(), [])


async def handle_list_position(request: web.Request):
    session = aiohttp_sqlalchemy.get_session(request)
    params = {key: request.rel_url.query[key] for key in request.rel_url.query.keys()}
    company: Company = request["company"]
    params["company_id"] = str(company.id)
    positions: List[Position] = await operations.paginated_list(session=session, model=Position, **params)
    return response.success_response([p.json() for p in positions], [])


async def handle_patch_position(request: web.Request):
    id = uuid.UUID(request.match_info.get("id"), version=4)
    payload = await utils.request_payload(request, PositionFormPatch)
    company: Company = request["company"]
    session = aiohttp_sqlalchemy.get_session(request)
    await session.execute(update(Position).where(
        (Position.id == id) & (Position.company_id == company.id) 
    ).values(**payload.model_dump(exclude_none=True)))
    await session.flush()
    result = await session.execute(select(Position).where(
        (Position.id == id) & (Position.company_id == company.id) 
    ))
    position = result.scalar_one_or_none()
    return response.success_response(position.json(), [])


async def handle_position(request: web.Request):
    id = uuid.UUID(request.match_info.get("id"), version=4)
    session = aiohttp_sqlalchemy.get_session(request)
    company: Company = request["company"]
    result = await session.execute(select(Position).where(
        (Position.id == id) & (Position.company_id == company.id) 
    ))
    position = result.scalar_one_or_none()
    if position is None:
        return response.error_response(None, ["Not found"], status=HTTPStatus.NOT_FOUND)
    return response.success_response(position.json(), [])


async def handle_delete_position(request: web.Request):
    id = uuid.UUID(request.match_info.get("id"), version=4)
    session = aiohttp_sqlalchemy.get_session(request)
    company: Company = request["company"]
    await session.execute(delete(Position).where(
        (Position == id) & (Position.company_id == company.id)
    ))
    return response.success_response(None, ["deleted"])
