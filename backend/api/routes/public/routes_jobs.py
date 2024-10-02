import logging

from aiohttp import web
from aiohttp_cache import cache

from pkg import response
from pkg.database import repositories

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_jobs_routes(app: web.Application):
    app.router.add_get("/api/positions", handle_positions_list)
    app.router.add_get("/api/positions/{id}", handle_position_detail)
    app.router.add_get("/api/companies", handle_companies_list)
    app.router.add_get("/api/companies/{company}", handle_company_detail)


@cache()
async def handle_positions_list(request: web.Request):
    async with request.app["session"] as session:
        # TODO: add kwargs:
        # - Show only positions with PositionStatus.ACTIVE
        positions = await repositories.get_positions(session)

    return response.success_response(
        {
            "positions": [p.json() for p in positions],
        },
        [],
    )


# @cache()
async def handle_position_detail(request: web.Request):
    position_id = request.match_info["id"]
    async with request.app["session"] as session:
        # TODO: add kwargs:
        # - Show only position with PositionStatus.ACTIVE
        position = await repositories.get_position(session, id=position_id)
        logger.info(position)
        return response.success_response(position.json(), [])


# @cache()
async def handle_companies_list(request: web.Request):
    async with request.app["session"] as session:
        companies = await repositories.get_companies(session)
    return response.success_response(
        {
            "companies": [c.json() for c in companies],
        },
        [],
    )


@cache()
async def handle_company_detail(request: web.Request):
    return response.success_response(None, [])
