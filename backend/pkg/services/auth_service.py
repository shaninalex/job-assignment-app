from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from api.routes.public.typing import ConfirmCodePayload, LoginPayload
from pkg import password, jwt
from pkg.consts import ConfirmStatusCode, AuthStatus, Role
from pkg.repositories.company_member_repository import CompanyMemberRepository
from pkg.repositories.company_repository import CompanyRepository
from pkg.repositories.confirm_codes_repository import ConfirmCodeRepository
from pkg.services.event_service import EventPublisher, Exchanges, RoutingKeys
from pkg.services.user_service import UserService
from pkg.settings import Config


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
        company_repository: CompanyRepository,
        confirm_codes_repository: ConfirmCodeRepository,
        event_service: EventPublisher,
        config: Config,
    ):
        self.config = config
        self.confirm_codes_repository = confirm_codes_repository
        self.event_service = event_service
        self.user_service = user_service
        self.company_repository = company_repository

    async def confirm(self, session: AsyncSession, payload: ConfirmCodePayload) -> bool:
        code = await self.confirm_codes_repository.get_code(session, payload.id, payload.code, ConfirmStatusCode.SENT)
        if code is None:
            raise Exception("confirm code is used or not found")

        if datetime.now() > code.expired_at:
            raise Exception("code is expired")

        user = await self.user_service.repository.get_by_id(session, code.user_id)
        if user is None:
            raise Exception("user does not exists or not found")

        user = await self.user_service.repository.update_by_id(
            session,
            user.id,
            {
                "confirmed": True,
                "active": True,
                "status": AuthStatus.ACTIVE,
            },
        )

        if not user:
            return False

        await self.confirm_codes_repository.update_by_id(session, code.id, {"status": ConfirmStatusCode.USED})
        await self.event_service.publish_event(
            Exchanges.ADMIN, RoutingKeys.COMPLETE_REGISTRATION_SUCCESS, {"user": user.json()}
        )
        await self.event_service.publish_event(
            Exchanges.EMAIL, RoutingKeys.COMPLETE_REGISTRATION_SUCCESS, {"user": user.json()}
        )
        return True

    async def login(self, session: AsyncSession, payload: LoginPayload):
        user = await self.user_service.repository.get_user(
            session, email=payload.email, active=True, status=AuthStatus.ACTIVE
        )
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

        resp = {
            "token": jwt.create_jwt_token(self.config.APP_SECRET, user),
            "user": user.json(),
        }

        if user.role in [Role.COMPANY_ADMIN, Role.COMPANY_MEMBER]:
            company = await self.company_repository.get_by_id(session, user.manager.company_id)
            if company:
                resp["company"] = company.json()

        await self.event_service.publish_event(Exchanges.LOG, RoutingKeys.USER_LOGIN, {"email": payload.email})
        return resp
