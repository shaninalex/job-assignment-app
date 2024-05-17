# Expiration check for jwt
# Docs:
#       https://pyjwt.readthedocs.io/en/latest/usage.html?highlight=expired#expiration-time-claim-exp

import jwt
from sqlalchemy import select
from aiohttp import web

from app.db import User
from app.settings import JWT_SECRET


@web.middleware
async def auth_middleware(request, handler):
    if "Authorization" not in request.headers:
        return web.json_response({"error": "unauthorized"}, status=401)

    token = request.headers["Authorization"].replace("Bearer ",  "")
    try:
        claims = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        if "sub" not in claims:
            return web.json_response({
                "error": "unauthorized",
                "message": "invalid claims",
            }, status=401)

        with request.app['db'] as session:
            query = select(User).where(User.id == claims["sub"])
            user: User = session.scalars(query).one()
            if not user:
                return web.json_response({
                    "error": "unauthorized",
                    "message": "invalid token",
                }, status=401)
            request["user"] = user

    except jwt.ExpiredSignatureError:
        return web.json_response({
            "error": "unauthorized",
            "message": "expired",
        }, status=401)
    except jwt.InvalidTokenError:
        return web.json_response({
            "error": "unauthorized",
            "message": "invalid token",
        }, status=401)

    return await handler(request)
