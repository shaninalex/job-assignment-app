from aiohttp import web

from pkg.app_keys import AppKeys
from pkg.repositories.company_member_repository import CompanyMemberRepository
from pkg.repositories.company_repository import CompanyRepository
from pkg.repositories.confirm_codes_repository import ConfirmCodeRepository
from pkg.repositories.position_repository import PositionRepository
from pkg.repositories.user_repository import UserRepository
from pkg.services.auth_service import AuthService
from pkg.services.event_service import EventPublisher
from pkg.services.position_service import PositionService
from pkg.services.user_service import UserService
from pkg.settings import Config


def initialize_dependencies(app: web.Application, config: Config):
    app[AppKeys.repository_user] = UserRepository()
    app[AppKeys.repository_company] = CompanyRepository()
    app[AppKeys.repository_company_member] = CompanyMemberRepository()
    app[AppKeys.repository_confirm_codes] = ConfirmCodeRepository()
    app[AppKeys.repository_position] = PositionRepository()
    app[AppKeys.service_events] = EventPublisher(rabbitmq_url=config.RABBIT_URL)
    app[AppKeys.service_position] = PositionService(
        repository=app[AppKeys.repository_position], event_service=app[AppKeys.service_events]
    )
    app[AppKeys.service_user] = UserService(
        repository=app[AppKeys.repository_user], event_service=app[AppKeys.service_events]
    )
    app[AppKeys.service_auth] = AuthService(
        config=config,
        company_member_repository=app[AppKeys.repository_company_member],
        company_repository=app[AppKeys.repository_company],
        confirm_codes_repository=app[AppKeys.repository_confirm_codes],
        user_service=app[AppKeys.service_user],
        event_service=app[AppKeys.service_events],
    )
