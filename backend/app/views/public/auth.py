from http import HTTPStatus

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, DatabaseError
from aiohttp import web
from pydantic import ValidationError
from app.db import User
from app.pkg.password import check_password
from app.pkg.jwt import create_jwt_token
from app.pkg.helpers import validation_error
from app.models import LoginPayload


def setup_auth_routes(app: web.Application):
    app.router.add_post("/api/auth/login", login_user)


async def login_user(request: web.Request) -> web.Response:
    data = await request.json()
    try:
        payload: LoginPayload = LoginPayload(**data)
    except ValidationError as e:
        error_messages = validation_error(e)
        return web.json_response(
            {
                "data": error_messages,
                "message": "There are some authentication errors",
                "success": False,
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    with request.app["db"] as session:
        try:
            user = session.scalars(
                select(User).where(User.email == payload.email)
            ).one()
            if check_password(payload.password, user.password):
                token = create_jwt_token(user)
                return web.json_response(
                    {
                        "data": token.model_dump(),
                        "message": "successfully authenticated",
                        "success": True,
                    },
                    status=HTTPStatus.OK,
                )
            return web.json_response(
                {"errors": "creadentials are incorrect"}, status=HTTPStatus.BAD_REQUEST
            )
        except NoResultFound:
            return web.json_response(
                {
                    "data": [
                        {
                            "field": "email",
                            "error_message": "User not found with given credentials",
                        }
                    ],
                    "message": "There are some authentication errors",
                    "success": False,
                },
                status=HTTPStatus.BAD_REQUEST,
            )
        except DatabaseError:
            return web.json_response(
                {
                    "data": [
                        {
                            "error_message": "Unable to process request",
                        }
                    ],
                    "message": "There are some authentication errors",
                    "success": False,
                },
                status=HTTPStatus.BAD_REQUEST,
            )
