from http import HTTPStatus
from typing import List

from sqlalchemy import select
from aiohttp import web
from app.db import Position, Skill


def setup_base_routes(app: web.Application):
    app.router.add_get('/api/public/positions', get_positions)
    app.router.add_get('/api/public/skills', get_skills)


async def get_skills(request: web.Request) -> web.Response:
    with request.app['db'] as session:
        skills = session.scalars(select(Skill))
        return web.json_response({
            "data": [s.json() for s in skills],
            "message": "123",
            "success": True,
        }, status=HTTPStatus.OK)


async def get_positions(request: web.Request) -> web.Response:
    with request.app['db'] as session:
        try:
            positions: List[Position] = session.scalars(select(Position))
            return web.json_response({
                "data": [p.json() for p in positions],
                "message": "",
                "success": True,
            })
        except Exception as e:
            return web.json_response({
                "data": {"errors": str(e)},
                "message": "There some errors",
                "success": False,
            }, status=HTTPStatus.BAD_REQUEST)
