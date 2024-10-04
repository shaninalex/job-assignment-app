from api.routes.public.typing import RegistrationPayload
from pkg.repositories.company_manager_repository import CompanyManagerRepository
from pkg.repositories.company_repository import CompanyRepository
from pkg.services.common import registration
from pkg.services.event_publisher import EventPublisher
from pkg.services.user_service import UserService


class AuthService:
    def __init__(
        self,
        user_service: UserService,
        company_manager_repository: CompanyManagerRepository,
        company_repository: CompanyRepository,
        event_service: EventPublisher,
    ):
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
