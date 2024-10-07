from aiohttp import web
from pydantic import ValidationError
from sqlalchemy.exc import DatabaseError
from pkg.response import error_response


@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)

    except DatabaseError as exc:
        # TODO: parse exception
        return error_response({"error": "database error handling not implemented"}, [])

    except ValueError as exc:
        # TODO: parse exception
        err = {"error": "wrong payload"}
        if isinstance(exc, ValidationError):
            err = exc.errors(include_url=False, include_input=False, include_context=False)
        return error_response(err, [])

    except Exception as exc:
        # TODO: parse exception
        err = {"error": str(exc) if isinstance(exc, Exception) else "Unknown error occurred"}
        return error_response(err, [])
