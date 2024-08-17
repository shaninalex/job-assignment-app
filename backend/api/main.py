import logging

from aiohttp import web
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from database.utils import database_url
from api.middlewares.utils import setup_middlewares
from api.settings import config
from api.routes import public


def setup_routes(app):
    public.setup_auth_routes(app)


async def init_app():
    app = web.Application()
    app["config"] = config()
    app["session"] = async_sessionmaker(
        create_async_engine(database_url(), echo=False), expire_on_commit=False
    )

    setup_middlewares(app)
    setup_routes(app)

    logging.info("Main app initialized")
    return app


def main():
    app = init_app()
    logging.basicConfig(level=logging.DEBUG)
    conf = config()
    web.run_app(app, port=conf["APP_PORT"])
