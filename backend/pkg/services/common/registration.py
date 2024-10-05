from abc import ABC, abstractmethod

from api.routes.public.typing import RegistrationPayload
from pkg.consts import Role
from pkg.models import Company, CompanyManager
from pkg.models import User
from pkg.repositories.company_manager_repository import CompanyManagerRepository
from pkg.repositories.company_repository import CompanyRepository
from pkg.services.event_publisher import EventPublisher, RoutingKeys, Exchanges
from pkg.services.user_service import UserService


class RegistrationStrategy(ABC):
    @abstractmethod
    async def register(self, payload: RegistrationPayload) -> User:
        pass


class CandidateRegistrationStrategy(RegistrationStrategy):
    def __init__(self, user_service: UserService, event_service: EventPublisher):
        self.user_service = user_service
        self.event_service = event_service

    async def register(self, payload: RegistrationPayload) -> User:
        user = await self.user_service.create_user(payload, Role.CANDIDATE)
        event_payload = {"user": user.json()}
        await self.event_service.publish_event(Exchanges.ADMIN, RoutingKeys.NEW_USER, event_payload)
        await self.event_service.publish_event(Exchanges.EMAIL, RoutingKeys.NEW_USER, event_payload)
        return user


class CompanyMemberRegistrationStrategy(RegistrationStrategy):
    def __init__(
        self,
        user_service: UserService,
        company_repository: CompanyRepository,
        company_member_repository: CompanyManagerRepository,
        event_service: EventPublisher,
    ):
        self.company_member_repository = company_member_repository
        self.company_repository = company_repository
        self.user_service = user_service
        self.event_service = event_service

    async def register(self, payload: RegistrationPayload) -> User:
        user = await self.user_service.create_user(payload, Role.COMPANY_MEMBER)
        company = await self.company_member_repository.get_by_id(1)
        await self.company_member_repository.create(CompanyManager(company=company, user=user))
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
        company_member_repository: CompanyManagerRepository,
        event_service: EventPublisher,
    ):
        self.user_service = user_service
        self.company_repository = company_repository
        self.company_member_repository = company_member_repository
        self.event_service = event_service

    async def register(self, payload: RegistrationPayload) -> User:
        user = await self.user_service.create_user(payload, Role.COMPANY_ADMIN)
        company = await self.company_repository.create(Company(name=payload.company_name))
        await self.company_member_repository.create(CompanyManager(company=company, user=user))
        await self.event_service.publish_event(
            Exchanges.ADMIN,
            RoutingKeys.NEW_COMPANY,
            {
                "user": user.json(),
                "company": company.json(),
            },
        )
        return user


class Registrator:
    def __init__(
        self,
        user_service: UserService,
        company_manager_repository: CompanyManagerRepository,
        company_repository: CompanyRepository,
        event_service: EventPublisher,
    ):
        self.user_service = user_service
        self.company_manager_repository = company_manager_repository
        self.company_repository = company_repository
        self.event_service = event_service

    def get_strategy(self, registration_type: Role) -> RegistrationStrategy:
        if registration_type == Role.COMPANY_ADMIN:
            return CompanyRegistrationStrategy(
                self.user_service, self.company_repository, self.company_manager_repository, self.event_service
            )

        if registration_type == Role.COMPANY_MEMBER:
            return CompanyMemberRegistrationStrategy(
                self.user_service, self.company_repository, self.company_manager_repository, self.event_service
            )

        if registration_type == Role.CANDIDATE:
            return CandidateRegistrationStrategy(self.user_service, self.event_service)
