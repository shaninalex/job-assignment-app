from http import HTTPStatus

from sqlalchemy import select
from aiohttp import web
from pydantic import ValidationError
from app.db import RecordNotFound, User
from app.pkg.password import check_password
from app.pkg.jwt import create_jwt_token
from app.models import LoginPayload


def setup_auth_routes(app: web.Application):
    app.router.add_post('/api/auth/login', login_user)


async def login_user(request: web.Request) -> web.Response:
    data = await request.json()
    try:
        payload: LoginPayload = LoginPayload(**data)
        with request.app['db'] as session:
            user = session.scalars(
                select(User).where(User.email == payload.email)
            ).one()
            if check_password(payload.password, user.password):
                token = create_jwt_token(user)
                return web.json_response({
                    "data": token.model_dump(),
                    "message": "successfully authenticated",
                    "success": True,
                }, status=HTTPStatus.OK)
            return web.json_response({"errors": "creadentials are incorrect"},
                                     status=HTTPStatus.BAD_REQUEST)
    except ValidationError as e:
        errors = e.errors()
        error_messages = []
        for error in errors:
            error_messages.append({
                "field": error["loc"][0],
                "error_message": error["msg"]
            })
        return web.json_response({
            "data": error_messages,
            "message": "There are some authentication errors",
            "success": False,
        }, status=HTTPStatus.BAD_REQUEST)
    except RecordNotFound:
        return web.json_response({
            "data": {
                "global": [
                    "creadentials are incorrect"
                ]
            },
            "message": "There are some authentication errors",
            "success": False,
        }, status=HTTPStatus.BAD_REQUEST)
    # return web.json_response({
    #     "data": None,
    #     "message": "Not implemented yet",
    #     "success": False,
    # }, status=HTTPStatus.BAD_REQUEST)

