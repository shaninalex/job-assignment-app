from http import HTTPStatus
from aiohttp import web
from pydantic import ValidationError
from sqlalchemy import select, delete
from sqlalchemy.exc import DatabaseError

from app.pkg.helpers import validation_error
from app.db import Candidate, CandidateSkill, CandidateSubmissions
from app.models import CandidateSubmissionPayload


def setup_candidates_routes(app: web.Application):
    app.router.add_get("/candidates", candidates_list_action)
    app.router.add_delete("/candidates/{id}", candidate_delete_action)
    app.router.add_post("/candidates/{id}/submit", candidate_submit_action)


async def candidate_delete_action(request: web.Request) -> web.Response:
    try:
        id = request.match_info.get("id")
    except ValueError:
        return web.json_response(
            {
                "data": [{"error_message": f"id {id} is not a valid id"}],
                "message": "Error",
                "success": False,
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    with request.app["db"] as session:
        try:
            # TODO: fix relationships to delete Candidate with
            # single command
            session.execute(
                delete(CandidateSkill).where(CandidateSkill.candidate_id == id)
            )
            session.execute(delete(Candidate).where(Candidate.id == id))
            session.commit()
            return web.json_response(
                {
                    "data": None,
                    "message": "Candidate successfully deleted",
                    "success": True,
                },
                status=HTTPStatus.OK,
            )
        except Exception as e:
            return web.json_response(
                {
                    "data": [{"error_message": str(e)}],
                    "message": "Unable to delete",
                    "success": True,
                },
                status=HTTPStatus.BAD_REQUEST,
            )


async def candidate_submit_action(request: web.Request) -> web.Response:
    # Submit/Reject action
    try:
        id = request.match_info.get("id")
    except ValueError:
        return web.json_response(
            {
                "data": [{"error_message": f"id {id} is not a valid id"}],
                "message": "Error",
                "success": False,
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    data = await request.json()
    try:
        payload: CandidateSubmissionPayload = CandidateSubmissionPayload(**data)
    except ValidationError as e:
        return web.json_response(
            {
                "data": validation_error(e),
                "message": "There are some errors",
                "success": False,
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    with request.app["db"] as session:
        try:
            candidate = session.query(Candidate).get(id)
            if not candidate:
                return web.json_response(
                    {
                        "data": None,
                        "message": "Candidate not found",
                        "success": False,
                    },
                    status=HTTPStatus.BAD_REQUEST,
                )

            submission = CandidateSubmissions(
                submitted=payload.submitted,
                reason=payload.reason,
                candidate_id=id,
                user_id=request["user"].id,
            )

            if not candidate.submitted:
                candidate.submitted = submission.submitted

            session.add(submission)
            session.commit()

            return web.json_response(
                {
                    "data": submission.to_json(),
                    "message": "Successfully submitted",
                    "success": True,
                },
                status=HTTPStatus.CREATED,
            )

        except DatabaseError as e:
            return web.json_response(
                {
                    "data": [{"error_message": "unable to submit", "details": str(e)}],
                    "message": "There are some errors",
                    "success": False,
                },
                status=HTTPStatus.BAD_REQUEST,
            )


async def candidates_list_action(request: web.Request) -> web.Response:
    with request.app["db"] as session:
        try:
            result = session.scalars(select(Candidate))
            return web.json_response(
                {
                    "data": [c.to_json() for c in result],
                    "message": "",
                    "success": True,
                },
                status=HTTPStatus.CREATED,
            )

        except Exception as e:
            return web.json_response(
                {
                    "data": [{"error_message": str(e)}],
                    "message": "There some error happend",
                    "success": False,
                },
                status=HTTPStatus.BAD_REQUEST,
            )
