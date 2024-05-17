from http import HTTPStatus
from aiohttp import web
from sqlalchemy import select
from app.db import Candidate


def setup_candidates_routes(app: web.Application):
    app.router.add_get('/candidates', candidates_list)


async def candidates_list(request: web.Request) -> web.Response:
    with request.app['db'] as session:
        try:
            result = session.scalars(select(Candidate))
            return web.json_response({
                "data": [c.to_json() for c in result],
                "message": "user was added",
                "success": True,
            }, status=HTTPStatus.CREATED)

        except Exception as e:
            return web.json_response({
                "data": {
                    "error": str(e),
                },
                "message": "There some error happend",
                "success": False,
            }, status=HTTPStatus.BAD_REQUEST)
