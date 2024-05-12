# Expiration check for jwt
# Docs:
#       https://pyjwt.readthedocs.io/en/latest/usage.html?highlight=expired#expiration-time-claim-exp

import jwt
from sqlalchemy import select
from aiohttp import web

from app import models
from app.db import users
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

        async with request.app['db'].acquire() as conn:
            query = select(users).where(users.c.id == claims["sub"])
            result = await conn.execute(query)
            data = await result.fetchone()
            if not data:
                return web.json_response({
                    "error": "unauthorized",
                    "message": "invalid token",
                }, status=401)
            user = models.User(**data)
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
