# Expiration check for jwt
# Docs:
#       https://pyjwt.readthedocs.io/en/latest/usage.html?highlight=expired#expiration-time-claim-exp

from typing import List
import jwt
from sqlalchemy import select
from aiohttp import web

from database import User, repositories
from globalTypes import AuthStatus, Role
from api.settings import JWT_SECRET


@web.middleware
async def auth_middleware(request, handler):
    if "Authorization" not in request.headers:
        return web.json_response({"error": "unauthorized"}, status=401)

    token = request.headers["Authorization"].replace("Bearer ", "")
    try:
        claims = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        if "sub" not in claims:
            return web.json_response(
                {
                    "error": "unauthorized",
                    "message": "invalid claims",
                },
                status=401,
            )

        async with request.app["session"] as session:
            user = await repositories.get_user(session, **{
                "id": claims["sub"],
                "active": True,
                "status": AuthStatus.ACTIVE,
            })

            if not user:
                return web.json_response(
                    {
                        "error": "unauthorized",
                        "message": "invalid token",
                    },
                    status=401,
                )

            request["user"] = user

    except jwt.ExpiredSignatureError:
        return web.json_response(
            {
                "error": "unauthorized",
                "message": "expired",
            },
            status=401,
        )
    except jwt.InvalidTokenError:
        return web.json_response(
            {
                "error": "unauthorized",
                "message": "invalid token",
            },
            status=401,
        )

    return await handler(request)


def roles_required(roles: List[Role]):
    @web.middleware
    async def role_required_inner(request, handler):
        if request["user"].role not in roles:
            return web.json_response(
                {
                    "error": "Permission",
                    "message": "Permission denied",
                },
                status=403,
            )

        return await handler(request)
    return role_required_inner

