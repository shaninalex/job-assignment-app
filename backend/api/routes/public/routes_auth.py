import uuid

import aiohttp_sqlalchemy
from aiohttp import web
from pydantic import BaseModel, EmailStr

from api.routes.public.typing import ConfirmCodePayload, LoginPayload
from pkg import password, response, utils
from pkg.app_keys import AppKeys
from pkg.common import operations
from pkg.consts import AuthStatus, ConfirmStatusCode, Role
from pkg.models.models import Company, CompanyManager, ConfirmCode, User
from pkg.services.event_service import Exchanges, RoutingKeys


def setup_auth_routes(app: web.Application):
    app.router.add_post("/api/auth/register", register_candidate)
    app.router.add_post("/api/auth/register/company", register_company)
    app.router.add_post("/api/auth/confirm", registration_confirm)
    app.router.add_post("/api/auth/login", login)


class CompanyRegistration(BaseModel, extra="forbid"):
    name: str
    email: EmailStr
    password: str
    password_confirm: str
    company_name: str
    company_email: str
    company_website: str


async def register_company(request: web.Request):
    session = aiohttp_sqlalchemy.get_session(request)
    payload: CompanyRegistration = await utils.request_payload(request, CompanyRegistration)

    if operations.is_user_exists(session, payload.email):
        return response.error_response(None, ["User already exists"])

    if operations.is_company_exists(session, payload.company_name, payload.company_email, payload.company_website):
        return response.error_response(None, ["Company already exists"])
    
    company = Company(
        name=payload.company_name,
        email=payload.company_email,
        website=payload.company_website,
    )
    user = User(
        id=uuid.uuid4(),
        email=payload.email,
        name=payload.name,
        role=Role.COMPANY_ADMIN,
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
        manager=CompanyManager(company=company)
    )

    session.add(company)
    session.add(user)
    await session.flush()
    await session.refresh(user)
    await session.refresh(company)

    await request.app[AppKeys.service_events].publish_event(
        Exchanges.ADMIN, RoutingKeys.NEW_COMPANY, {"user": user.json(), "company": company.json()}
    )
    await request.app[AppKeys.service_events].publish_event(
        Exchanges.EMAIL, RoutingKeys.NEW_COMPANY, {"user": user.json(), "company": company.json()}
    )
    return response.success_response({"user": user.json(), "company": company.json()}, [])


class CandidateRegistration(BaseModel, extra="forbid"):
    name: str
    email: EmailStr
    password: str
    password_confirm: str


async def register_candidate(request: web.Request):
    session = aiohttp_sqlalchemy.get_session(request)
    payload = await utils.request_payload(request, CandidateRegistration)

    if operations.is_user_exists(session, payload.email):
        return response.error_response(None, ["User already exists"])

    user = User(
        id=uuid.uuid4(),
        email=payload.email,
        name=payload.name,
        role=Role.CANDIDATE,
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
    )

    session.add(user)
    await session.flush()
    await session.refresh(user)

    await request.app[AppKeys.service_events].publish_event(
        Exchanges.ADMIN, RoutingKeys.NEW_USER, {"user": user.json()}
    )
    await request.app[AppKeys.service_events].publish_event(
        Exchanges.EMAIL, RoutingKeys.NEW_USER, {"user": user.json()}
    )
    return response.success_response({"user": user.json()}, [])


async def registration_confirm(request: web.Request):
    session = aiohttp_sqlalchemy.get_session(request)
    payload = await utils.request_payload(request, ConfirmCodePayload)
    result = await request.app[AppKeys.service_auth].confirm(session, payload)
    return response.success_response(result, [])


async def login(request: web.Request):
    session = aiohttp_sqlalchemy.get_session(request)
    payload = await utils.request_payload(request, LoginPayload)
    jwt_token = await request.app[AppKeys.service_auth].login(session, payload)
    return response.success_response(jwt_token, [])
