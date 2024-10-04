from aiohttp import web
from dependency_injector.wiring import Provide

from api.routes.public.typing import RegistrationPayload
from pkg import response, utils
from pkg.container import Container
from pkg.services.auth_service import AuthService


def setup_auth_routes(app: web.Application):
    app.router.add_post("/api/auth/register", handle_registration)
    app.router.add_post("/api/auth/confirm", handle_registration_confirm)
    app.router.add_post("/api/auth/login", handle_login)


async def handle_registration(
    request: web.Request,
    auth_service: AuthService = Provide[Container.auth_service],
):
    payload = await utils.request_payload(request, RegistrationPayload)
    if isinstance(payload, web.Response):
        return payload
    user = await auth_service.registration(payload)
    return response.success_response({"user": user.json()}, [])

async def handle_registration_confirm(request: web.Request):
    return response.success_response({}, [])
    # payload = await utils.request_payload(request, ConfirmCodePayload)
    # if isinstance(payload, web.Response):
    #     return payload
    #
    # async with request.app["session"] as session:
    #     try:
    #         code = await repositories.get_confirm_code(
    #             session, payload.id, payload.code, ConfirmStatusCode.CREATED
    #         )
    #         if code is None:
    #             return response.error_response(None, messages=["Wrong credentials"])
    #
    #         if datetime.now() > code.expired_at:
    #             return response.error_response(None, messages=["Code is expired"])
    #
    #         # Call confirm_user function to confirm the user and update the status
    #         user = await repositories.confirm_user(session, code)
    #         if user is None:
    #             return response.error_response(None, messages=["Wrong credentials"])
    #
    #         return response.success_response(
    #             payload=None, messages=["Successfully confirmed."]
    #         )
    #
    #     except SQLAlchemyError as e:
    #         await session.rollback()
    #
    #         errs = errors.parse_sqlalchemy_error(e)
    #         return response.error_response(errs, messages=[])


async def handle_login(request: web.Request):
    return response.success_response({}, [])
    # payload = await utils.request_payload(request, LoginPayload)
    # if isinstance(payload, web.Response):
    #     return payload
    #
    # async with request.app["session"] as session:
    #     user = await repositories.get_user(
    #         session,
    #         **{
    #             "email": payload.email,
    #             "active": True,
    #             "status": AuthStatus.ACTIVE,
    #         }
    #     )
    #
    #     if user is None:
    #         return response.error_response(None, messages=["Wrong credentials"])
    #
    #     if not password.check_password(payload.password, user.password_hash):
    #         return response.error_response(None, messages=["Wrong credentials"])
    #
    #     company = None
    #     if user.role in [Role.COMPANY_ADMIN, Role.COMPANY_MANAGER]:
    #         company = await repositories.get_company(
    #             session, id=user.manager.company_id
    #         )
    #
    # resp = {
    #     "token": jwt.create_jwt_token(user),
    #     "user": user.json(),
    # }
    # if company:
    #     resp["company"] = company.json()
    #
    # return response.success_response(payload=resp, messages=[])
