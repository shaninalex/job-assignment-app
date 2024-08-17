from http import HTTPStatus
from aiohttp import web
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from database.repositories import registration
from globalTypes import RegistrationType
from api.types import RegisterPayload
from api.pkg import jwt


def setup_auth_routes(app: web.Application):
    app.router.add_post("/api/auth/register", handle_registration)


async def handle_registration(request: web.Request) -> web.Response:
    data = await request.json()
    try:
        payload = RegisterPayload().load(data)
    except ValidationError as err:
        return web.json_response({"errors": err.messages}, status=HTTPStatus.BAD_REQUEST)

    async with request.app["session"] as session:
        try:
            if payload["type"] == RegistrationType.CANDIDATE:
                # TODO: send rabbitmq message about new candidate
                return web.json_response({"data": "register candidate"}, status=HTTPStatus.OK)
            if payload["type"] == RegistrationType.COMPANY:
                company, auth, member = await registration.create_company(session, payload)
                # TODO: send rabbitmq message about new company
                return web.json_response({
                    "token": jwt.create_jwt_token(auth),
                    "extra": {
                        "role": "member role admin"
                    }
                }, status=HTTPStatus.OK)

        except SQLAlchemyError as e:
            if "duplicate key value violates unique" in e.args[0]:
                return web.json_response({"errors": ["Account with this email already exists"]}, status=HTTPStatus.BAD_REQUEST)
            return web.json_response({"errors": [str(e)]}, status=HTTPStatus.BAD_REQUEST)
