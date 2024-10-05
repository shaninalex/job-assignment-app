from dependency_injector import containers, providers

from pkg.database import async_session
from pkg.repositories.company_manager_repository import CompanyManagerRepository
from pkg.repositories.company_repository import CompanyRepository
from pkg.repositories.confirm_codes_repository import ConfirmCodeRepository
from pkg.repositories.user_repository import UserRepository
from pkg.services.auth_service import AuthService
from pkg.services.event_publisher import EventPublisher
from pkg.services.user_service import UserService
from pkg.settings import CONFIG


class Container(containers.DeclarativeContainer):
    """
    Container class encapsulates the dependency injection configuration.
    """

    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.routes.company.routes_company",
            "api.routes.public.routes_auth",
            "api.routes.public.routes_jobs",
        ]
    )

    # provide async session
    session = providers.Singleton(async_session)

    # initialize user repository ( only repository communicate with database )
    user_repository: UserRepository = providers.Factory(UserRepository, session=session)
    company_repository: CompanyRepository = providers.Factory(CompanyRepository, session=session)
    company_member_repository: CompanyManagerRepository = providers.Factory(CompanyManagerRepository, session=session)
    confirm_codes_repository: ConfirmCodeRepository = providers.Factory(ConfirmCodeRepository, session=session)

    # initialize rabbitmq service
    event_service: EventPublisher = providers.Singleton(
        EventPublisher,
        rabbitmq_url=CONFIG.RABBIT_URL,
    )

    # initialize user service
    user_service: UserService = providers.Singleton(
        UserService,
        repository=user_repository,
        event_service=event_service,
    )

    auth_service: AuthService = providers.Singleton(
        AuthService,
        user_service=user_service,
        company_manager_repository=company_member_repository,
        company_repository=company_repository,
        event_service=event_service,
        confirm_codes_repository=confirm_codes_repository,
    )
