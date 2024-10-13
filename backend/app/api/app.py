from fastapi import FastAPI

from app.api.exceptions import lifespan, apply_exception_handlers
from app.api.routers import auth, health, company, public


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    apply_exception_handlers(app)
    # init rabbitmq event publisher

    # add routers
    app.include_router(health.router)
    app.include_router(public.router)
    app.include_router(auth.router)
    app.include_router(company.router)

    return app
