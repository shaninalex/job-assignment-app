import logging

from aiohttp import web
from aiohttp_cache import cache

from pkg import response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_jobs_routes(app: web.Application):
    app.router.add_get("/api/positions", handle_positions_list)
    app.router.add_get("/api/positions/{id}", handle_position_detail)
    app.router.add_get("/api/companies", handle_companies_list)
    app.router.add_get("/api/companies/{company}", handle_company_detail)


@cache()
async def handle_positions_list(request: web.Request):
    return response.success_response({}, [])


@cache()
async def handle_position_detail(request: web.Request):
    return response.success_response({}, [])


@cache()
async def handle_companies_list(request: web.Request):
    return response.success_response({}, [])


@cache()
async def handle_company_detail(request: web.Request):
    return response.success_response({}, [])
