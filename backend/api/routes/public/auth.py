from pika.adapters.blocking_connection import BlockingChannel

from http import HTTPStatus
from aiohttp import web
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from database.repositories import registration
from globalTypes import RegistrationType
from api.types import RegisterForm, RegistrationPayload
from pkg import jwt
from pkg import rabbitmq


def setup_auth_routes(app: web.Application):
    app.router.add_post("/api/auth/register", handle_registration)
    app.router.add_post("/api/auth/confirm", handle_registration_confirm)


async def handle_registration(request: web.Request) -> web.Response:
    """
    Example payloads. For candidate:
    {
        "name": "Alex",
        "email": "info17@person.com",
        "password": "123",
        "password_confirm": "123",
        "type": "CANDIDATE"
    }

    For company:
    {
        "name": "John Snow",
        "companyName": "Snow inc.",
        "email": "info17@person.com",
        "password": "123",
        "password_confirm": "123",
        "type": "COMPANY"
    }
    """
    data = await request.json()
    try:
        reg_form = RegisterForm()
        input_data = reg_form.load(data)
        payload = RegistrationPayload(**input_data)

    except ValidationError as err:
        return web.json_response(
            {"errors": err.messages}, status=HTTPStatus.BAD_REQUEST
        )

    async with request.app["session"] as session:
        channel: BlockingChannel = request.app["channel"]
        try:
            if payload["type"] == RegistrationType.CANDIDATE:
                auth, candidate = await registration.create_candidate(session, payload)
                rabbitmq.create_new_candidate(channel, candidate)
                await rabbitmq.confirm_account(session, channel, auth, candidate.name)
                return web.json_response(
                    {
                        "token": jwt.create_jwt_token(auth),
                        "account": candidate.json(),
                    },
                    status=HTTPStatus.OK,
                )

            if payload["type"] == RegistrationType.COMPANY:
                company, auth, member = await registration.create_company(
                    session, payload
                )
                rabbitmq.create_new_company(channel, company, member)
                await rabbitmq.confirm_account(session, channel, auth, member.name)
                return web.json_response(
                    {
                        "token": jwt.create_jwt_token(auth),
                        "account": member.json(),
                        "company": company.json(),
                    },
                    status=HTTPStatus.OK,
                )

        except SQLAlchemyError as e:
            if "duplicate key value violates unique" in e.args[0]:
                return web.json_response(
                    {"errors": ["Account with this email already exists"]},
                    status=HTTPStatus.BAD_REQUEST,
                )
            return web.json_response(
                {"errors": [str(e)]}, status=HTTPStatus.BAD_REQUEST
            )


async def handle_registration_confirm(request: web.Request) -> web.Response:
    return web.json_response({}, status=HTTPStatus.OK)
