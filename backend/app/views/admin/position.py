from http import HTTPStatus

from aiohttp import web
from pydantic import ValidationError
from app.db import Skill, Position, PositionSkill
from app.models import Skill as SkillModel, Position as PositionModel
from app.pkg.dbhelpers import get_or_create_skills
from app.pkg.helpers import validation_error


def setup_position_routes(app: web.Application):
    app.router.add_post('/positions', positions_create)
    app.router.add_get('/positions/{id}', positions_get)
    app.router.add_delete('/positions/{id}', positions_delete)
    app.router.add_patch('/positions/{id}', positions_patch)
    app.router.add_post('/skills', skills_create)
    app.router.add_delete('/skills/{id}', skills_delete)
    app.router.add_patch('/skills/{id}', skills_patch)


async def positions_create(request: web.Request) -> web.Response:
    data = await request.json()
    try:
        payload: PositionModel = PositionModel(**data)
        with request.app['db'] as session:
            try:
                # create skills list
                skills = get_or_create_skills(session, payload.skills)
                position: Position = Position(
                    name=payload.name,
                    description=payload.description,
                    skills=[PositionSkill(skill_id=s.id) for s in skills],
                )
                session.add(position)
                session.commit()

                return web.json_response({
                    "data": position.json(),
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

    with request.app['db'] as session:
        try:
            position: Position = session.query(Position).get(
                int(request.match_info.get('id', "0"))
            )
            return web.json_response({
                "data": position.json(),
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
    if "id" not in request.match_info:
        return web.json_response({
            "data": {"errors": "id is missing"},
            "message": "There some errors",
            "success": False,
        }, status=HTTPStatus.BAD_REQUEST)

    with request.app['db'] as session:
        pos_to_delete = session.query(Position).get(
            int(request.match_info.get('id', "0"))
        )
        if pos_to_delete:
            session.delete(pos_to_delete)
            session.commit()
            return web.json_response({
                "data": None,
                "message": "Successfully deleted",
                "success": True,
            }, status=HTTPStatus.OK)
        else:
            return web.json_response({
                "data": None,
                "message": "Position with given id does not exist",
                "success": False,
            }, status=HTTPStatus.NOT_FOUND)


async def positions_patch(request):
    return web.json_response({
        "data": [],
        "message": "",
        "success": True,
    })


async def skills_create(request):
    request_data = await request.json()
    try:
        payload = Skill(**request_data)
        with request.app['db'] as session:
            try:
                skill = Skill(name=payload.name)
                session.add(skill)
                session.commit()
                return web.json_response({
                    "data": skill.json(),
                    "message": "skill successfully created",
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

    with request.app['db'] as session:
        skill_to_delete = session.query(Skill).get(
            int(request.match_info.get('id', "0"))
        )
        if skill_to_delete:
            session.delete(skill_to_delete)
            session.commit()
            return web.json_response({
                "data": None,
                "message": "Successfully deleted",
                "success": True,
            }, status=HTTPStatus.OK)
        else:
            return web.json_response({
                "data": None,
                "message": "Skill with given id does not exist",
                "success": False,
            }, status=HTTPStatus.NOT_FOUND)


async def skills_patch(request):
    if "id" not in request.match_info:
        return web.json_response({
            "data": {"errors": "id is missing"},
            "message": "There some errors",
            "success": False,
        }, status=HTTPStatus.BAD_REQUEST)

    request_data = await request.json()
    try:
        SkillModel(**request_data)  # validate payload
        with request.app['db'] as session:
            try:
                skill_to_update = session.query(Skill).get(
                    int(request.match_info.get('id', "0"))
                )
                if skill_to_update:
                    skill_to_update.name = request_data['name']
                    session.commit()
                    return web.json_response({
                        "data": skill_to_update.json(),
                        "message": "",
                        "success": True,
                    }, status=HTTPStatus.OK)
                else:
                    return web.json_response({
                        "data": None,
                        "message": "Skill with given id does not exist",
                        "success": False,
                    }, status=HTTPStatus.NOT_FOUND)

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

