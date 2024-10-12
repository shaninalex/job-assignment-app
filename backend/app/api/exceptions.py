from fastapi.exceptions import RequestValidationError
from pika.exceptions import AMQPConnectionError
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from loguru import logger
from pydantic import ValidationError
from starlette.responses import JSONResponse

from app.api.serializers import APIResponse
from app.db.session import sessionmanager
from app.exceptions.exceptions import ServiceError

SERVICE_ERROR_MESSAGE = "A service seems to be down, try again later."
SERVICE_ERROR_PAYLOAD_VALIDATION = "Form contain some errors."


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager.engine is not None:
        await sessionmanager.close()


def apply_exception_handlers(app: FastAPI):

    # input payload validation error
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=APIResponse(
                error=exc.errors(),
                message=["Payload validation error"],
                status=False
            ).model_dump()
        )

    # this is not db connection error. It's general connection error
    app.add_exception_handler(
        exc_class_or_status_code=ConnectionRefusedError, handler=database_connection_exception_handler()
    )
    app.add_exception_handler(exc_class_or_status_code=AMQPConnectionError, handler=amqp_connection_exception_handler())
    app.add_exception_handler(
        exc_class_or_status_code=ServiceError,
        handler=get_service_error_handler(),
    )
    app.add_exception_handler(
        exc_class_or_status_code=422,
        handler=create_validation_error_handler(),
    )


def amqp_connection_exception_handler():
    async def exception_handler(_, exc) -> JSONResponse:
        logger.error(f"AMQP connection error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=APIResponse(message=[SERVICE_ERROR_MESSAGE], status=False).model_dump()
        )

    return exception_handler


def database_connection_exception_handler():
    async def exception_handler(_, exc) -> JSONResponse:
        logger.error(f"Database connection error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=APIResponse(message=[SERVICE_ERROR_MESSAGE], status=False).model_dump()
        )

    return exception_handler


def get_service_error_handler():
    return create_exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR, SERVICE_ERROR_MESSAGE)


def create_exception_handler(status_code: int, initial_detail: str):
    detail = {"message": initial_detail}

    async def exception_handler(_, exc) -> JSONResponse:
        logger.error(exc)
        if exc.message:
            detail["message"] = exc.message

        # hide internal technical details from api
        # if exc.name:
        #     detail["message"] = f"{detail['message']} [{exc.name}]"

        return JSONResponse(
            status_code=status_code,
            content=APIResponse(message=[detail["message"]], status=False).model_dump()
        )

    return exception_handler


def create_validation_error_handler():
    async def exception_handler(_, exc) -> JSONResponse:
        logger.error(f"Form validation error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=APIResponse(
                message=[SERVICE_ERROR_PAYLOAD_VALIDATION],
                status=False
            ).model_dump()
        )

    return exception_handler


