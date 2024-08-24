import json
from http import HTTPStatus

from aiohttp import web
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from api.types import RegistrationPayload, ConfirmCodePayload
from database import repositories
from globalTypes import RegistrationType, ConfirmStatusCode
from pkg import jwt, errors
from pkg import rabbitmq


def setup_auth_routes(app: web.Application):
    app.router.add_post("/api/auth/register", handle_registration)
    app.router.add_post("/api/auth/confirm", handle_registration_confirm)


async def handle_registration(request: web.Request):
    data = await request.json()
    try:
        payload = RegistrationPayload(**data)
    except ValidationError as err:
        return web.json_response(
            json.loads(
                err.json(include_url=False, include_input=False, include_context=False)
            ),
            status=HTTPStatus.BAD_REQUEST,
        )

    async with request.app["session"] as session:
        try:
            if payload.type == RegistrationType.CANDIDATE:
                user, candidate = await repositories.create_candidate(session, payload)
                rabbitmq.admin_create_new_candidate(request.app["mq"], user.json())
                rabbitmq.email_confirm_account(
                    request.app["mq"], user.json(), user.codes[0].json()
                )
                return web.json_response(
                    {
                        "token": jwt.create_jwt_token(user),
                        "user": user.json(),
                        "candidate": candidate.json(),
                    },
                    status=HTTPStatus.OK,
                )

            if payload.type == RegistrationType.COMPANY:
                if not payload.companyName:
                    return web.json_response(
                        [
                            errors.create_form_error(
                                "companyName",
                                "Company name is required on company registration",
                            )
                        ],
                        status=HTTPStatus.BAD_REQUEST,
                    )

                company, user, member = await repositories.create_company(
                    session, payload
                )
                rabbitmq.admin_create_new_company(
                    request.app["mq"], company.json(), member.json(), user.json()
                )
                rabbitmq.email_confirm_account(
                    request.app["mq"], user.json(), user.codes[0].json()
                )
                return web.json_response(
                    {
                        "token": jwt.create_jwt_token(user),
                        "user": user.json(),
                        "company": company.json(),
                    },
                    status=HTTPStatus.OK,
                )

        except SQLAlchemyError as e:
            if "duplicate key value violates unique" in e.args[0]:
                # TODO: find out what field trigger this error.
                # Because companyName also should be unique, but
                # this error displays as an email field error"""
                return web.json_response(
                    [
                        errors.create_form_error(
                            "email", "Account with this email already exists"
                        )
                    ],
                    status=HTTPStatus.BAD_REQUEST,
                )
            return web.json_response(
                {"errors": [str(e)]}, status=HTTPStatus.BAD_REQUEST
            )


async def handle_registration_confirm(request: web.Request):
    data = await request.json()
    try:
        payload = ConfirmCodePayload(**data)
    except ValidationError as err:
        return web.json_response(
            json.loads(
                err.json(include_url=False, include_input=False, include_context=False)
            ),
            status=HTTPStatus.BAD_REQUEST,
        )

    async with request.app["session"] as session:
        try:
            code = await repositories.get_confirm_code(session, payload.id, payload.code, ConfirmStatusCode.CREATED)
            if code is None:
                return web.json_response(
                    {"error": "No record found"}, status=HTTPStatus.NOT_FOUND
                )

            # TODO: is expired - return expired error and delete code.

            if code.code != payload.code:
                return web.json_response(
                    [errors.create_form_error("code", "Code mismatch")],
                    status=HTTPStatus.NOT_FOUND,
                )

            # Call confirm_user function to confirm the user and update the status
            user = await repositories.confirm_user(session, code)
            if user is None:
                return web.json_response(
                    {"error": "User not found"}, status=HTTPStatus.NOT_FOUND
                )

            # Prepare payloads and publish success messages to RabbitMQ
            rabbitmq_payloads = user.json()
            rabbitmq.email_confirm_account_success(request.app["mq"], rabbitmq_payloads)
            rabbitmq.admin_confirm_account_success(request.app["mq"], rabbitmq_payloads)

            return web.json_response({"status": "confirmed"}, status=HTTPStatus.OK)

        except SQLAlchemyError as e:
            await session.rollback()
            return web.json_response(
                {"errors": [str(e)]}, status=HTTPStatus.BAD_REQUEST
            )
        
