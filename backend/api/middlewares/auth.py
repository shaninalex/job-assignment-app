# Expiration check for jwt
# Docs:
#       https://pyjwt.readthedocs.io/en/latest/usage.html?highlight=expired#expiration-time-claim-exp

from http import HTTPStatus
from typing import List
import jwt
from sqlalchemy import select
from aiohttp import web

from database import User, repositories
from globalTypes import AuthStatus, Role
from api.settings import JWT_SECRET
from pkg import response


@web.middleware
async def auth_middleware(request, handler):
    if "Authorization" not in request.headers:
        return response.error_response(None, status=HTTPStatus.UNAUTHORIZED)

    token = request.headers["Authorization"].replace("Bearer ", "")
    try:
        claims = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        if "sub" not in claims:
            return response.error_response(None, ["Invalid claims"], status=HTTPStatus.UNAUTHORIZED)

        async with request.app["session"] as session:
            user = await repositories.get_user(session, **{
                "id": claims["sub"],
                "active": True,
                "status": AuthStatus.ACTIVE,
            })

            if not user:
                return response.error_response(None, ["User not found"], status=HTTPStatus.UNAUTHORIZED)

            if user.manager:
                company = await repositories.get_company(session, **{"id": user.manager.company_id})
                request["company"] = company

            request["user"] = user

    except jwt.ExpiredSignatureError:
        return response.error_response(None, ["Expired"], status=HTTPStatus.UNAUTHORIZED)

    except jwt.InvalidTokenError:
        return response.error_response(None, ["Invalid token"], status=HTTPStatus.UNAUTHORIZED)

    return await handler(request)


def roles_required(roles: List[Role]):
    @web.middleware
    async def role_required_inner(request, handler):
        if request["user"].role not in roles:
            return response.error_response(None, ["Invalid token"], status=HTTPStatus.FORBIDDEN)
        return await handler(request)

    return role_required_inner

