from aiohttp import web

from pkg.repositories.company_manager_repository import CompanyManagerRepository
from pkg.repositories.company_repository import CompanyRepository
from pkg.repositories.confirm_codes_repository import ConfirmCodeRepository
from pkg.repositories.user_repository import UserRepository
from pkg.services.auth_service import AuthService
from pkg.services.event_publisher import EventPublisher
from pkg.services.user_service import UserService
from pkg.settings import Config


def initialize_dependencies(app: web.Application, config: Config):
    app["repository_user"] = UserRepository()
    app["repository_company"] = CompanyRepository()
    app["repository_company_member"] = CompanyManagerRepository()
    app["repository_confirm_codes"] = ConfirmCodeRepository()
    app["service_events"] = EventPublisher(rabbitmq_url=config.RABBIT_URL)
    app["service_user"] = UserService(repository=app["repository_user"], event_service=app["service_events"])
    app["service_auth"] = AuthService(
        config=config,
        company_manager_repository=app["repository_company_member"],
        company_repository=app["repository_company"],
        confirm_codes_repository=app["repository_confirm_codes"],
        user_service=app["service_user"],
        event_service=app["service_events"],
    )
