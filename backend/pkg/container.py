from dependency_injector import containers, providers

from pkg.database import async_session
from pkg.repositories.company_manager_repository import CompanyManagerRepository
from pkg.repositories.company_repository import CompanyRepository
from pkg.repositories.user_repository import UserRepository
from pkg.services.auth_service import AuthService
from pkg.services.event_publisher import EventPublisher
from pkg.services.user_service import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.routes.company.routes_company",
            "api.routes.public.routes_auth",
            "api.routes.public.routes_jobs",
        ]
    )

    # provide async session
    session = providers.Factory(async_session)

    # initialize user repository ( only repository communicate with database )
    user_repository: UserRepository = providers.Factory(UserRepository, session=session)
    company_repository: CompanyRepository = providers.Factory(CompanyRepository, session=session)
    company_member_repository: CompanyManagerRepository = providers.Factory(CompanyManagerRepository, session=session)

    # initialize rabbitmq service
    event_service: EventPublisher = providers.Singleton(
        EventPublisher,
        rabbitmq_url="amqp://guest:guest@localhost/",
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
    )
