import aiohttp_sqlalchemy
from aiohttp import web

from api.routes.public.typing import RegistrationPayload, ConfirmCodePayload, LoginPayload
from pkg import response, utils


def setup_auth_routes(app: web.Application):
    app.router.add_post("/api/auth/register", registration)
    app.router.add_post("/api/auth/confirm", registration_confirm)
    app.router.add_post("/api/auth/login", login)


async def registration(request: web.Request):
    session = aiohttp_sqlalchemy.get_session(request)
    payload = await utils.request_payload(request, RegistrationPayload)
    user = await request.app["service_auth"].registration(session, payload)
    return response.success_response({"user": user.json()}, [])

async def registration_confirm(request: web.Request):
    session = aiohttp_sqlalchemy.get_session(request)
    payload = await utils.request_payload(request, ConfirmCodePayload)
    result = await request.app["service_auth"].confirm(session, payload)
    return response.success_response(result, [])

async def login(request: web.Request):
    session = aiohttp_sqlalchemy.get_session(request)
    payload = await utils.request_payload(request, LoginPayload)
    jwt_token = await request.app["service_auth"].login(session, payload)
    return response.success_response(jwt_token, [])
