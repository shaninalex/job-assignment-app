from aiohttp import web
from dependency_injector.wiring import Provide, inject

from api.routes.public.typing import RegistrationPayload, ConfirmCodePayload, LoginPayload
from pkg import response, utils
from pkg.container import Container
from pkg.services.auth_service import AuthService


@inject
def setup_auth_routes(app: web.Application, auth_service: AuthService = Provide[Container.auth_service]):
    handler = AuthHandler(auth_service=auth_service)
    app.router.add_post("/api/auth/register", handler.registration)
    app.router.add_post("/api/auth/confirm", handler.registration_confirm)
    app.router.add_post("/api/auth/login", handler.login)


class AuthHandler:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    async def registration(self, request: web.Request):
        payload = await utils.request_payload(request, RegistrationPayload)
        user = await self.auth_service.registration(payload)
        return response.success_response({"user": user.json()}, [])

    async def registration_confirm(self, request: web.Request):
        payload = await utils.request_payload(request, ConfirmCodePayload)
        result = await self.auth_service.confirm(payload)
        return response.success_response(result, [])

    async def login(self, request: web.Request):
        payload = await utils.request_payload(request, LoginPayload)
        jwt_token = await self.auth_service.login(payload)
        return response.success_response(jwt_token, [])
