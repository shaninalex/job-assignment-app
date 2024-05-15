from http import HTTPStatus

from aiohttp import web
from pydantic import ValidationError

from app.models import Skill, Position
from app.pkg.helpers import validation_error
from app.repositories import skills, pos


def setup_position_routes(app: web.Application):
    app.router.add_get('/positions', positions_list)
    app.router.add_post('/positions', positions_create)
    app.router.add_get('/positions/{id}', positions_get)
    app.router.add_delete('/positions/{id}', positions_delete)
    app.router.add_patch('/positions/{id}', positions_patch)
    app.router.add_get('/skills', skills_list)
    app.router.add_post('/skills', skills_create)
    app.router.add_delete('/skills/{id}', skills_delete)
    app.router.add_patch('/skills/{id}', skills_patch)


async def positions_list(request):
    return web.json_response({
        "data": [],
        "message": "",
        "success": True,
    })


async def positions_create(request: web.Request) -> web.Response:
    data = await request.json()
    try:
        payload: Position = Position(**data)
        async with request.app['db'].acquire() as conn:
            try:
                result = pos.create(conn, payload)
                return web.json_response({
                    "data": result.model_dump(),
                    "message": "",
                    "success": True,
                })

            except Exception as e:
                return web.json_response({
                    "data": {"errors": str(e)},
                    "message": "There some errors",
                    "success": False,
                }, status=HTTPStatus.BAD_REQUEST)

    except ValidationError as e:
        error_messages = validation_error(e)
        return web.json_response({
            "data": error_messages,
            "message": "There some errors",
            "success": False,
        }, status=HTTPStatus.BAD_REQUEST)


async def positions_get(request):
    if "id" not in request.match_info:
        return web.json_response({
            "data": {"errors": "id is missing"},
            "message": "There some errors",
            "success": False,
        }, status=HTTPStatus.BAD_REQUEST)

    id = int(request.match_info.get('id', "0"))
    async with request.app['db'].acquire() as conn:
        try:
            result = pos.get(conn, id)
            return web.json_response({
                "data": result.model_dump(),
                "message": "",
                "success": True,
            })

        except Exception as e:
            return web.json_response({
                "data": {"errors": str(e)},
                "message": "There some errors",
                "success": False,
            }, status=HTTPStatus.BAD_REQUEST)


async def positions_delete(request):
    return web.json_response({
        "data": [],
        "message": "",
        "success": True,
    })


async def positions_patch(request):
    return web.json_response({
        "data": [],
        "message": "",
        "success": True,
    })


async def skills_list(request):
    async with request.app['db'].acquire() as conn:
        s = await skills.all(conn)
        return web.json_response({
            "data": [item.model_dump() for item in s],
            "message": "123",
            "success": True,
        }, status=HTTPStatus.OK)


async def skills_create(request):
    request_data = await request.json()
    try:
        payload = Skill(**request_data)
        async with request.app['db'].acquire() as conn:
            try:
                out = await skills.create(conn, payload)
                return web.json_response({
                    "data": out.model_dump(),
                    "message": "",
                    "success": True,
                }, status=HTTPStatus.OK)
            except Exception as e:
                return web.json_response({
                    "data": {"errors": str(e)},
                    "message": "There some errors",
                    "success": False,
                }, status=HTTPStatus.BAD_REQUEST)

    except ValidationError as e:
        error_messages = validation_error(e)
        return web.json_response({
            "data": error_messages,
            "message": "There some errors",
            "success": False,
        }, status=HTTPStatus.BAD_REQUEST)


async def skills_delete(request: web.Request):
    if "id" not in request.match_info:
        return web.json_response({
            "data": {"errors": "id is missing"},
            "message": "There some errors",
            "success": False,
        }, status=HTTPStatus.BAD_REQUEST)

    id = int(request.match_info.get('id', "0"))
    async with request.app['db'].acquire() as conn:
        await skills.delete(conn, id)
        return web.json_response({
            "data": None,
            "message": "Successfully deleted",
            "success": True,
        }, status=HTTPStatus.OK)


async def skills_patch(request):
    if "id" not in request.match_info:
        return web.json_response({
            "data": {"errors": "id is missing"},
            "message": "There some errors",
            "success": False,
        }, status=HTTPStatus.BAD_REQUEST)

    id = int(request.match_info.get('id', "0"))

    request_data = await request.json()
    try:
        payload = Skill(**request_data)
        payload.id = id
        async with request.app['db'].acquire() as conn:
            try:
                out = await skills.patch(conn, payload)
                return web.json_response({
                    "data": out.model_dump(),
                    "message": "",
                    "success": True,
                }, status=HTTPStatus.OK)
            except Exception as e:
                return web.json_response({
                    "data": {"errors": str(e)},
                    "message": "There some errors",
                    "success": False,
                }, status=HTTPStatus.BAD_REQUEST)

    except ValidationError as e:
        error_messages = validation_error(e)
        return web.json_response({
            "data": error_messages,
            "message": "There some errors",
            "success": False,
        }, status=HTTPStatus.BAD_REQUEST)
