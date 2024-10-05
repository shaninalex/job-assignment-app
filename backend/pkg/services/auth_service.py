from datetime import datetime

from api.routes.public.typing import RegistrationPayload, ConfirmCodePayload, LoginPayload
from pkg import password, jwt
from pkg.consts import ConfirmStatusCode, AuthStatus, Role
from pkg.repositories.company_manager_repository import CompanyManagerRepository
from pkg.repositories.company_repository import CompanyRepository
from pkg.repositories.confirm_codes_repository import ConfirmCodeRepository
from pkg.services.common import registration
from pkg.services.event_publisher import EventPublisher, Exchanges, RoutingKeys
from pkg.services.user_service import UserService


class AuthService:
    """
    AuthService
    -----------
    A service class responsible for handling user authentication, including registration,
    confirmation of registration codes, and login processes.

    Methods
    -------
    __init__(user_service, company_manager_repository, company_repository, confirm_codes_repository, event_service)
        Initializes the AuthService with required dependencies.

    registration(payload)
        Registers a user based on the provided payload.

    confirm(payload) -> bool
        Confirms a registration using the provided confirmation code payload.

    login(payload)
        Authenticates a user based on login credentials provided in the payload.
    """

    def __init__(
        self,
        user_service: UserService,
        company_manager_repository: CompanyManagerRepository,
        company_repository: CompanyRepository,
        confirm_codes_repository: ConfirmCodeRepository,
        event_service: EventPublisher,
    ):
        self.confirm_codes_repository = confirm_codes_repository
        self.event_service = event_service
        self.company_manager_repository = company_manager_repository
        self.user_service = user_service
        self.company_repository = company_repository

        self._registration = registration.Registrator(
            user_service, company_manager_repository, company_repository, event_service
        )

    async def registration(self, payload: RegistrationPayload):
        strategy = self._registration.get_strategy(payload.type)
        return await strategy.register(payload)

    async def confirm(self, payload: ConfirmCodePayload) -> bool:
        code = await self.confirm_codes_repository.get_code(payload.id, payload.code, ConfirmStatusCode.CREATED)
        if code is None:
            raise Exception("confirm code is used or not found")

        if datetime.now() > code.expired_at:
            raise Exception("code is expired")

        user = await self.user_service.repository.get_by_id(code.user_id)
        if user is None:
            raise Exception("user does not exists or not found")

        user = await self.user_service.repository.update_by_id(
            user.id,
            {
                "confirmed": True,
                "active": True,
                "status": AuthStatus.ACTIVE,
            },
        )

        await self.confirm_codes_repository.update_by_id(code.id, {"status": ConfirmStatusCode.USED})
        await self.event_service.publish_event(
            Exchanges.ADMIN, RoutingKeys.COMPLETE_REGISTRATION_SUCCESS, {"user": user.json()}
        )
        await self.event_service.publish_event(
            Exchanges.EMAIL, RoutingKeys.COMPLETE_REGISTRATION_SUCCESS, {"user": user.json()}
        )
        return True

    async def login(self, payload: LoginPayload):
        user = await self.user_service.repository.get_user(email=payload.email, active=True, status=AuthStatus.ACTIVE)
        if user is None:
            await self.event_service.publish_event(
                Exchanges.LOG, RoutingKeys.USER_LOGIN_FAILED, {"email": payload.email, "reason": "User not found"}
            )
            raise Exception("wrong credentials")

        if not password.check_password(payload.password, user.password_hash):
            await self.event_service.publish_event(
                Exchanges.LOG, RoutingKeys.USER_LOGIN_FAILED, {"email": payload.email, "reason": "Wrong password"}
            )
            return Exception("invalid password")

        company = None
        if user.role in [Role.COMPANY_ADMIN, Role.COMPANY_MEMBER]:
            company = await self.company_repository.get_by_id(user.manager.company_id)

        resp = {
            "token": jwt.create_jwt_token(user),
            "user": user.json(),
        }

        if company:
            resp["company"] = company.json()

        await self.event_service.publish_event(Exchanges.LOG, RoutingKeys.USER_LOGIN, {"email": payload.email})
        return resp