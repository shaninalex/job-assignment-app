from aiohttp import web
from pkg import response
from database import repositories


def setup_jobs_routes(app: web.Application):
    app.router.add_get("/api/positions", handle_positions_list)
    app.router.add_get("/api/positions/{id}", handle_position_detail)
    app.router.add_get("/api/company", handle_companies_list)
    app.router.add_get("/api/company/{company}", handle_company_detail)


async def handle_positions_list(request: web.Request):
    async with request.app["session"] as session:
        positions = await repositories.get_positions(session) 

    return response.success_response({
        "positions": [p.json() for p in positions],
    }, [])

async def handle_position_detail(request: web.Request):
    return response.success_response(None, [])

async def handle_companies_list(request: web.Request):
    return response.success_response(None, [])

async def handle_company_detail(request: web.Request):
    return response.success_response(None, [])
