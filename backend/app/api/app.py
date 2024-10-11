from fastapi import FastAPI

from app.api.routers import auth, health


def create_app() -> FastAPI:
    app = FastAPI()

    # init rabbitmq event publisher
    # add global middlewares

    # add routers
    app.include_router(health.router)
    app.include_router(auth.router)
    return app

