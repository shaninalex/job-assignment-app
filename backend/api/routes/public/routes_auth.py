from datetime import datetime

from aiohttp import web
from sqlalchemy.exc import SQLAlchemyError

from pkg import jwt, errors, rabbitmq, password, response, utils
from pkg.consts import Role, RegistrationType, ConfirmStatusCode, AuthStatus
from pkg.database import repositories
from ._types import RegistrationPayload, ConfirmCodePayload, LoginPayload


def setup_auth_routes(app: web.Application):
    app.router.add_post("/api/auth/register", handle_registration)
    app.router.add_post("/api/auth/confirm", handle_registration_confirm)
    app.router.add_post("/api/auth/login", handle_login)


async def handle_registration(request: web.Request):
    payload = await utils.request_payload(request, RegistrationPayload)
    if isinstance(payload, web.Response):
        return payload

    async with request.app["session"] as session:
        try:
            if payload.type == RegistrationType.CANDIDATE:
                user, candidate = await repositories.create_candidate(session, payload)
                rabbitmq.admin_create_new_candidate(request.app["mq"], user.json())
                rabbitmq.email_confirm_account(
                    request.app["mq"], user.json(), user.codes[0].json()
                )
                return response.success_response(None, ["Successfully registered."])
            else:
                company, user, member = await repositories.create_company(
                    session, payload
                )
                rabbitmq.admin_create_new_company(
                    request.app["mq"], company.json(), member.json(), user.json()
                )
                rabbitmq.email_confirm_account(
                    request.app["mq"], user.json(), user.codes[0].json()
                )
                return response.success_response(
                    None, ["Successfully registered company."]
                )

        except SQLAlchemyError as e:
            await session.rollback()
            errs = errors.parse_sqlalchemy_error(e)
            return response.error_response(errs)


async def handle_registration_confirm(request: web.Request):
    payload = await utils.request_payload(request, ConfirmCodePayload)
    if isinstance(payload, web.Response):
        return payload

    async with request.app["session"] as session:
        try:
            code = await repositories.get_confirm_code(
                session, payload.id, payload.code, ConfirmStatusCode.CREATED
            )
            if code is None:
                return response.error_response(None, messages=["Wrong credentials"])

            if datetime.now() > code.expired_at:
                return response.error_response(None, messages=["Code is expired"])

            # Call confirm_user function to confirm the user and update the status
            user = await repositories.confirm_user(session, code)
            if user is None:
                return response.error_response(None, messages=["Wrong credentials"])

            # Prepare payloads and publish success messages to RabbitMQ
            rabbitmq_payloads = user.json()
            rabbitmq.email_confirm_account_success(request.app["mq"], rabbitmq_payloads)
            rabbitmq.admin_confirm_account_success(request.app["mq"], rabbitmq_payloads)

            return response.success_response(None, ["Successfully confirmed."])

        except SQLAlchemyError as e:
            await session.rollback()

            errs = errors.parse_sqlalchemy_error(e)
            return response.error_response(errs)


async def handle_login(request: web.Request):
    payload = await utils.request_payload(request, LoginPayload)
    if isinstance(payload, web.Response):
        return payload

    async with request.app["session"] as session:
        user = await repositories.get_user(
            session,
            **{
                "email": payload.email,
                "active": True,
                "status": AuthStatus.ACTIVE,
            }
        )

        if user is None:
            return response.error_response(None, messages=["Wrong credentials"])

        if not password.check_password(payload.password, user.password_hash):
            return response.error_response(None, messages=["Wrong credentials"])

        company = None
        if user.role in [Role.COMPANY_ADMIN, Role.COMPANY_MANAGER]:
            company = await repositories.get_company(
                session, id=user.manager.company_id
            )

    resp = {
        "token": jwt.create_jwt_token(user),
        "user": user.json(),
    }
    if company:
        resp["company"] = company.json()

    return response.success_response(resp)
