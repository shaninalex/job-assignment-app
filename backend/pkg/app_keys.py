from enum import StrEnum

from aiohttp import web


class AppKeys(StrEnum):
    repository_user = "repository_user"
    repository_company = "repository_company"
    repository_company_member = "repository_company_member"
    repository_confirm_codes = "repository_confirm_codes"
    repository_position = "repository_position"
    service_events = "service_events"
    # service_position = "service_position"
    service_user = "service_user"
    service_auth = "service_auth"


def share_keys(app: web.Application, app2: web.Application):
    for key in [e for e in AppKeys]:
        app2[key] = app[key]
