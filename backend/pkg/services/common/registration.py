from abc import ABC, abstractmethod
from deprecated import deprecated

from sqlalchemy.ext.asyncio import AsyncSession

from api.routes.public.typing import RegistrationPayload
from pkg.consts import Role
from pkg.models import Company, CompanyManager
from pkg.models import User
from pkg.repositories.company_member_repository import CompanyMemberRepository
from pkg.repositories.company_repository import CompanyRepository
from pkg.services.event_service import EventPublisher, RoutingKeys, Exchanges
from pkg.services.user_service import UserService


class RegistrationStrategy(ABC):
    @abstractmethod
    async def register(self, session: AsyncSession, payload: RegistrationPayload) -> User:
        pass


class CandidateRegistrationStrategy(RegistrationStrategy):
    def __init__(self, user_service: UserService, event_service: EventPublisher):
        self.user_service = user_service
        self.event_service = event_service

    async def register(self, session: AsyncSession, payload: RegistrationPayload) -> User:
        user = await self.user_service.create_user(session, payload, Role.CANDIDATE)
        event_payload = {"user": user.json()}
        await self.event_service.publish_event(Exchanges.ADMIN, RoutingKeys.NEW_USER, event_payload)
        await self.event_service.publish_event(Exchanges.EMAIL, RoutingKeys.NEW_USER, event_payload)
        return user


class CompanyMemberRegistrationStrategy(RegistrationStrategy):
    def __init__(
        self,
        user_service: UserService,
        company_repository: CompanyRepository,
        company_member_repository: CompanyMemberRepository,
        event_service: EventPublisher,
    ):
        self.company_member_repository = company_member_repository
        self.company_repository = company_repository
        self.user_service = user_service
        self.event_service = event_service

    async def register(self, session: AsyncSession, payload: RegistrationPayload) -> User:
        user = await self.user_service.create_user(session, payload, Role.COMPANY_MEMBER)
        company = await self.company_member_repository.get_by_id(session, user.id)
        await self.company_member_repository.create(session, CompanyManager(company=company, user=user))
        await self.event_service.publish_event(
            Exchanges.ADMIN,
            RoutingKeys.NEW_COMPANY_MEMBER,
            {
                "user": user.json(),
                "company": company,
            },
        )
        return user


class CompanyRegistrationStrategy(RegistrationStrategy):
    def __init__(
        self,
        user_service: UserService,
        company_repository: CompanyRepository,
        company_member_repository: CompanyMemberRepository,
        event_service: EventPublisher,
    ):
        self.user_service = user_service
        self.company_repository = company_repository
        self.company_member_repository = company_member_repository
        self.event_service = event_service

    async def register(self, session: AsyncSession, payload: RegistrationPayload) -> User:
        user = await self.user_service.create_user(session, payload, Role.COMPANY_ADMIN)
        company = await self.company_repository.create(session, Company(name=payload.company_name))
        await self.company_member_repository.create(session, CompanyManager(company=company, user=user))
        await self.event_service.publish_event(
            Exchanges.ADMIN,
            RoutingKeys.NEW_COMPANY,
            {
                "user": user.json(),
                "company": company.json(),
            },
        )
        return user


@deprecated(
    reason="Not flexible enough to register new users, companies and members",
    category=DeprecationWarning
)
class Registrator:
    """
    Deprecated: Not flexible enough to register new users, companies and members
    """
    def __init__(
        self,
        user_service: UserService,
        company_member_repository: CompanyMemberRepository,
        company_repository: CompanyRepository,
        event_service: EventPublisher,
    ):
        self.user_service = user_service
        self.company_member_repository = company_member_repository
        self.company_repository = company_repository
        self.event_service = event_service

    def get_strategy(self, registration_type: Role) -> RegistrationStrategy:
        if registration_type == Role.COMPANY_ADMIN:
            return CompanyRegistrationStrategy(
                self.user_service, self.company_repository, self.company_member_repository, self.event_service
            )

        if registration_type == Role.COMPANY_MEMBER:
            return CompanyMemberRegistrationStrategy(
                self.user_service, self.company_repository, self.company_member_repository, self.event_service
            )

        if registration_type == Role.CANDIDATE:
            return CandidateRegistrationStrategy(self.user_service, self.event_service)
