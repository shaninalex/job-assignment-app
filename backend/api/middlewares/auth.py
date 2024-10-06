# Expiration check for jwt
# Docs:
#       https://pyjwt.readthedocs.io/en/latest/usage.html?highlight=expired#expiration-time-claim-exp

from http import HTTPStatus
from typing import List

import aiohttp_sqlalchemy
import jwt
from aiohttp import web

from pkg import response
from pkg.app_keys import AppKeys
from pkg.consts import AuthStatus
from pkg.consts import Role
from pkg.models import User
from pkg.settings import Config


@web.middleware
async def auth_middleware(request, handler):

    if "Authorization" not in request.headers:
        return response.error_response(None, ["Unauthorized"], status=HTTPStatus.UNAUTHORIZED)

    token = request.headers["Authorization"].replace("Bearer ", "")
    config: Config = request.app["config"]
    session = aiohttp_sqlalchemy.get_session(request)
    try:
        claims = jwt.decode(token, config.APP_SECRET, algorithms=["HS256"])
        if "sub" not in claims:
            return response.error_response(None, ["Invalid claims"], status=HTTPStatus.UNAUTHORIZED)
        
        user: User = await request.app[AppKeys.repository_user].get_user(
            session, id=claims["sub"], active=True, status=AuthStatus.ACTIVE
        )
        
        if not user:
            return response.error_response(None, ["User not found"], status=HTTPStatus.UNAUTHORIZED)

        if user.manager:
            company = await request.app[AppKeys.repository_company].get_by_id(session, user.manager.company_id)
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
