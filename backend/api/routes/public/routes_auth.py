from pika.adapters.blocking_connection import BlockingChannel
import json

from http import HTTPStatus
from aiohttp import web
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, delete

from database import ConfirmCode, User
from database.repositories import registration
from globalTypes import RegistrationType
from api.types import RegistrationPayload, ConfirmCodePayload
from pkg import jwt, errors
from pkg import rabbitmq


def setup_auth_routes(app: web.Application):
    app.router.add_post("/api/auth/register", handle_registration)
    app.router.add_post("/api/auth/confirm", handle_registration_confirm)


async def handle_registration(request: web.Request) -> web.Response:
    data = await request.json()
    try:
        payload = RegistrationPayload(**data)
    except ValidationError as err:
        return web.json_response(
            json.loads(err.json(include_url=False, include_input=False, include_context=False)), status=HTTPStatus.BAD_REQUEST
        )

    async with request.app["session"] as session:
        channel: BlockingChannel = request.app["channel"]
        try:
            if payload.type == RegistrationType.CANDIDATE:
                user, candidate = await registration.create_candidate(session, payload)
                rabbitmq.create_new_candidate(channel, user)
                await rabbitmq.confirm_account(session, channel, user, user.codes[0])
                return web.json_response(
                    {
                        "token": jwt.create_jwt_token(user),
                        "user": user.json(),
                    },
                    status=HTTPStatus.OK,
                )

            if payload.type == RegistrationType.COMPANY:
                if not payload.companyName:
                    return web.json_response(
                        [errors.create_form_error(
                            "companyName", "Company name is required on company registration")],
                        status=HTTPStatus.BAD_REQUEST,
                    )

                company, user, member = await registration.create_company(
                    session, payload
                )
                rabbitmq.create_new_company(channel, company, member, user)
                await rabbitmq.confirm_account(session, channel, user, user.codes[0])
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
                """TODO: find out what field trigger this error. Because companyName also should be unique, but
                this error displays as an email field error"""
                return web.json_response(
                    [errors.create_form_error(
                        "email", "Account with this email already exists")],
                    status=HTTPStatus.BAD_REQUEST,
                )
            return web.json_response(
                {"errors": [str(e)]}, status=HTTPStatus.BAD_REQUEST
            )


async def handle_registration_confirm(request: web.Request) -> web.Response:
    data = await request.json()
    try:
        code = ConfirmCodePayload(**data)
    except ValidationError as err:
        return web.json_response(
            json.loads(err.json(include_url=False, include_input=False, include_context=False)), status=HTTPStatus.BAD_REQUEST
        )

    async with request.app["session"] as session:
        query = select(ConfirmCode).where(ConfirmCode.id == code.id)
        result = await session.execute(query)
        fetched = result.fetchone()
        if fetched is None:
            return web.json_response({"error": "No record found"}, status=HTTPStatus.NOT_FOUND)

        _code = fetched[0]
        # TODO: is expired - return expired error and delete code.

        if _code.code != code.code:
            return web.json_response(
                [errors.create_form_error(
                    "code", "Code mismatch")],
                status=HTTPStatus.NOT_FOUND)

        result = await session.execute(select(User).where(User.id == _code.user_id))
        users = result.fetchone()
        user = users[0]
        user.confirmed = True

        await session.execute(delete(ConfirmCode).where(ConfirmCode.id == code.id))
        await session.commit()

        # TODO:
        # - send email to user about successfully confirmation account
        # - send rabbitmq event to admin about confirmation
        return web.json_response({"status": "confirmed"}, status=HTTPStatus.OK)
