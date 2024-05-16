from http import HTTPStatus
from aiohttp import web
from typing import List

from app.repositories import candidates


def setup_candidates_routes(app: web.Application):
    app.router.add_get('/candidates', candidates_list)


async def candidates_list(request: web.Request) -> web.Response:
    async with request.app['db'].acquire() as conn:
        try:
            result = await candidates.all(conn)
            out: List[dict] = []
            for c in result:
                out.append(c.to_json())
            return web.json_response({
                "data": out,
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
