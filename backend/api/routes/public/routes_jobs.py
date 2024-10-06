from http import HTTPStatus
import logging
from typing import List

from aiohttp import web
from aiohttp_cache import cache
import aiohttp_sqlalchemy

from pkg import response
from pkg.app_keys import AppKeys
from pkg.models.models import Position
from pkg.settings import DEBUG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_jobs_routes(app: web.Application):
    app.router.add_get("/api/positions", handle_positions_list)
    app.router.add_get("/api/positions/{id}", handle_position_detail)
    app.router.add_get("/api/companies", handle_companies_list)
    app.router.add_get("/api/companies/{company}", handle_company_detail)


# @cache(unless=DEBUG)
async def handle_positions_list(request: web.Request):
    session = aiohttp_sqlalchemy.get_session(request)
    service = request.app[AppKeys.service_position]
    params = {key: request.rel_url.query[key] for key in request.rel_url.query.keys()}
    positions: List[Position] = await service.list(session, **params)
    return response.success_response([p.json() for p in positions], [])


# @cache(unless=DEBUG)
async def handle_position_detail(request: web.Request):
    position_id = request.match_info.get('id')
    session = aiohttp_sqlalchemy.get_session(request)
    service = request.app[AppKeys.service_position]
    position: Position = await service.repository.get_by_id(session, position_id)
    if not position:
        return response.error_response(None, ["Position not found"], status=HTTPStatus.NOT_FOUND)
    return response.success_response(position.json(), [])


# @cache(unless=DEBUG)
async def handle_companies_list(request: web.Request):
    return response.success_response({}, [])


# @cache(unless=DEBUG)
async def handle_company_detail(request: web.Request):
    return response.success_response({}, [])
