from http import HTTPStatus
from typing import List

from aiohttp import web
from pydantic import ValidationError

from sqlalchemy import select
from app.db import Role, User
from app.models import AdminCreateUserPayload
from app.pkg.helpers import validation_error
from app.pkg.password import get_hashed_password


def setup_admin_routes(app: web.Application):
    app.router.add_post("/manage/create-user", create_user)
    app.router.add_get("/manage/users-list", users_list)


async def users_list(request):
    if request["user"].role is not Role.admin:
        return web.json_response(
            {
                "data": [{"error_message": "You have not enough permissions"}],
                "message": "Request forbidden",
                "success": False,
            },
            status=HTTPStatus.FORBIDDEN,
        )

    with request.app["db"] as session:
        users = session.scalars(select(User))
        out: List[dict] = [u.json() for u in users]
        return web.json_response(
            {
                "data": out,
                "message": "",
                "success": True,
            },
            status=HTTPStatus.OK,
        )


async def create_user(request):
    if request["user"].role is not Role.admin:
        return web.json_response(
            {
                "data": [{"error_message": "You have not enough permissions"}],
                "message": "Request forbidden",
                "success": False,
            },
            status=HTTPStatus.FORBIDDEN,
        )

    data = await request.json()
    try:
        payload: AdminCreateUserPayload = AdminCreateUserPayload(**data)

        with request.app["db"] as session:
            try:
                hashed_password = get_hashed_password(payload.password)
                user: User = User(email=payload.email, password=hashed_password)
                session.add(user)
                session.commit()
                return web.json_response(
                    {
                        "data": user.json(),
                        "message": "user was added",
                        "success": True,
                    },
                    status=HTTPStatus.CREATED,
                )

            except Exception as e:
                return web.json_response(
                    {
                        "data": [{"error_message": str(e)}],
                        "message": "There some error happend",
                        "success": False,
                    },
                    status=HTTPStatus.BAD_REQUEST,
                )

    except ValidationError as e:
        return web.json_response(
            {
                "data": validation_error(e),
                "message": "There some errors",
                "success": False,
            },
            status=HTTPStatus.BAD_REQUEST,
        )
