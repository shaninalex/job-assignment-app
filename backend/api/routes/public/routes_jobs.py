from http import HTTPStatus
import logging
from typing import List
import uuid

from aiohttp import web
from aiohttp_cache import cache
import aiohttp_sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from pkg import response
from pkg.app_keys import AppKeys
from pkg.common import operations
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
# async def handle_positions_list(request: web.Request):
#     session = aiohttp_sqlalchemy.get_session(request)
#     params = {key: request.rel_url.query[key] for key in request.rel_url.query.keys()}
#     # positions: List[Position] = await operations.paginated_list(session=session, model=Position, **params)
#     stmt = select(Position)
#     filters = {}
#     limit = None
#     offset = None
#     for k in params.keys():
#         if k == "limit":
#             limit = params[k]
#         elif k == "offset":
#             offset = params[k]
#         else:
#             filters[k] = params[k]

#     if limit is not None:
#         stmt = stmt.limit(limit)
#     if offset is not None:
#         stmt = stmt.offset(offset)

#     if len(filters) != 0:
#         for key, value in filters.items():
#             stmt = stmt.where(getattr(Position, key) == value)
#     result = await session.execute(stmt)
#     positions = result.scalars().all()
#     return response.success_response([p.json() for p in positions], [])
#     # return response.success_response(params, [])

async def handle_positions_list(request: web.Request):
    # Get the async session from the request (ensure it's AsyncSession)
    session: AsyncSession = aiohttp_sqlalchemy.get_session(request)
    
    # Extract query parameters
    params = {key: request.rel_url.query[key] for key in request.rel_url.query.keys()}
    
    # Start building the statement
    stmt = select(Position).options(selectinload(Position.company))
    filters = {}
    limit = None
    offset = None

    # Parse parameters
    for k, v in params.items():
        if k == "limit":
            limit = int(v)  # Convert to int
        elif k == "offset":
            offset = int(v)  # Convert to int
        else:
            filters[k] = v

    # Apply limit and offset
    if limit is not None:
        stmt = stmt.limit(limit)
    if offset is not None:
        stmt = stmt.offset(offset)

    # Apply filters dynamically
    if filters:
        for key, value in filters.items():
            stmt = stmt.where(getattr(Position, key) == value)

    # Execute the query with async session
    result = await session.execute(stmt)
    for row in result.all():
        p = row._asdict()
        logger.info(p["Position"].__dict__)
    
    # Return response with positions as JSON
    # return response.success_response([p._mapping for p in positions], [])
    return response.success_response([], [])


# @cache(unless=DEBUG)
async def handle_position_detail(request: web.Request):
    id = uuid.UUID(request.match_info.get("id"), version=4)
    session = aiohttp_sqlalchemy.get_session(request)
    result = await session.execute(select(Position).where(Position.id == id))
    position = result.scalar_one_or_none()
    if position is None:
        return response.error_response(None, ["Not found"], status=HTTPStatus.NOT_FOUND)
    return response.success_response(position.json(), [])

# @cache(unless=DEBUG)
async def handle_companies_list(request: web.Request):
    return response.success_response({}, [])


# @cache(unless=DEBUG)
async def handle_company_detail(request: web.Request):
    return response.success_response({}, [])
