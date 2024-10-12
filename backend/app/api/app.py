from fastapi import FastAPI

from app.api.routers import auth, health, company
from app.api.exceptions import lifespan, apply_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    apply_exception_handlers(app)
    # init rabbitmq event publisher
    # add global middlewares

    # add routers
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(company.router)

    return app
