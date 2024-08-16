from http import HTTPStatus

from aiohttp import web
from pydantic import ValidationError
from uuid import uuid4, UUID
from sqlalchemy.exc import IntegrityError

from app.db import Candidate, CandidateSkill
from app.models import ApplyPayload
from app.pkg.dbhelpers import get_or_create_skills
from app.pkg.helpers import validation_error


def setup_apply_routes(app: web.Application):
    app.router.add_post("/api/apply/form", apply_form)
    app.router.add_patch("/api/apply/form", form_patch_action)
    app.router.add_get("/api/apply/result", get_result)


async def form_patch_action(request: web.Request) -> web.Response:
    if "id" not in request.rel_url.query:
        return web.json_response(
            {
                "data": "",
                "message": "Your submission id was not provided",
                "success": True,
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    try:
        submission_id = UUID(request.rel_url.query["id"], version=4)
    except ValueError:
        return web.json_response(
            {
                "data": [{"error_message": "invalid id"}],
                "message": "Your submission id was invalid",
                "success": False,
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    with request.app["db"] as session:
        try:
            candidate: Candidate = (
                session.query(Candidate)
                .filter(Candidate.secret == str(submission_id))
                .first()
            )

            if not candidate:
                return web.json_response(
                    {
                        "data": {"errors": "not found"},
                        "message": "Submission with given hash not found",
                        "success": False,
                    },
                    status=HTTPStatus.NOT_FOUND,
                )

            data = await request.json()
            try:
                payload: ApplyPayload = ApplyPayload(**data)
            except ValidationError as e:
                error_messages = validation_error(e)
                return web.json_response(
                    {
                        "data": error_messages,
                        "message": "There some errors",
                        "success": False,
                    },
                    status=HTTPStatus.BAD_REQUEST,
                )

            skills = get_or_create_skills(session, payload.skills)
            candidate.skills = []
            candidate.skills = [CandidateSkill(skill_id=s.id) for s in skills]

            candidate.name = payload.name
            candidate.email = payload.email
            candidate.phone = payload.phone
            candidate.about = payload.about
            candidate.position_id = payload.position_id

            session.commit()

            return web.json_response(
                {
                    "data": candidate.to_json(),
                    "message": "",
                    "success": True,
                },
                status=HTTPStatus.OK,
            )

        except Exception as e:
            print(e)
            return web.json_response(
                {
                    "data": {"errors": str(e)},
                    "message": "There some errors",
                    "success": False,
                },
                status=HTTPStatus.BAD_REQUEST,
            )


async def apply_form(request: web.Request) -> web.Response:
    data = await request.json()
    try:
        with request.app["db"] as session:
            payload: ApplyPayload = ApplyPayload(**data)
            try:
                skills = get_or_create_skills(session, payload.skills)
                candidate: Candidate = Candidate(
                    name=payload.name,
                    email=payload.email,
                    phone=payload.phone,
                    about=payload.about,
                    secret=str(uuid4()),
                    position_id=payload.position_id,
                    skills=[CandidateSkill(skill_id=s.id) for s in skills],
                )
                session.add(candidate)
                session.commit()
                return web.json_response(
                    {
                        "data": candidate.to_json(),
                        "message": "Your request was successfully applied",
                        "success": True,
                    },
                    status=HTTPStatus.OK,
                )
            except IntegrityError:
                return web.json_response(
                    {
                        "data": [{"error_message": "already submitted"}],
                        "message": "There some errors",
                        "success": False,
                    },
                    status=HTTPStatus.BAD_REQUEST,
                )
            except Exception as e:
                return web.json_response(
                    {
                        "data": {"errors": str(e)},
                        "message": "There some errors",
                        "success": False,
                    },
                    status=HTTPStatus.BAD_REQUEST,
                )

    except ValidationError as e:
        error_messages = validation_error(e)
        return web.json_response(
            {
                "data": error_messages,
                "message": "There some errors",
                "success": False,
            },
            status=HTTPStatus.BAD_REQUEST,
        )


async def get_result(request: web.Request) -> web.Response:
    if "id" not in request.rel_url.query:
        return web.json_response(
            {
                "data": "",
                "message": "Your submission id was not provided",
                "success": True,
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    try:
        submission_id = UUID(request.rel_url.query["id"], version=4)
        with request.app["db"] as session:
            try:
                candidate: Candidate = (
                    session.query(Candidate)
                    .filter(Candidate.secret == str(submission_id))
                    .first()
                )
                if candidate:
                    message = "Your request was successfully submitted and assigned"
                    if not candidate.submitted:
                        message = "Your request was not submitted yet. Wait a little bit more, or update your skills"

                    return web.json_response(
                        {
                            "data": candidate.to_json(),
                            "message": message,
                            "success": True,
                        },
                        status=HTTPStatus.OK,
                    )
                else:
                    return web.json_response(
                        {
                            "data": {"errors": "not found"},
                            "message": "Submission with given hash not found",
                            "success": False,
                        },
                        status=HTTPStatus.NOT_FOUND,
                    )

            except Exception as e:
                return web.json_response(
                    {
                        "data": {"errors": str(e)},
                        "message": "There some errors",
                        "success": False,
                    },
                    status=HTTPStatus.BAD_REQUEST,
                )

    except ValueError:
        return web.json_response(
            {
                "data": {"errors": "invalid id"},
                "message": "Your submission id was invalid",
                "success": False,
            },
            status=HTTPStatus.BAD_REQUEST,
        )
