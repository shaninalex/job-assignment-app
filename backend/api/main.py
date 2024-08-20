import logging

import pika
from aiohttp import web
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from database.utils import database_url
from api.middlewares.utils import setup_middlewares
from api.settings import config
from api.routes import public


def setup_routes(app):
    public.setup_auth_routes(app)


async def init_app():
    app = web.Application()
    app["config"] = config()
    session = async_sessionmaker(
        create_async_engine(database_url(), echo=False), expire_on_commit=False
    )
    app["session"] = session()

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            "localhost", credentials=pika.PlainCredentials("guest", "guest")
        )
    )

    app["connection"] = connection
    app["channel"] = connection.channel()
    app.on_shutdown.append(close_rmq_connection)

    setup_middlewares(app)
    setup_routes(app)

    logging.info("Main app initialized")
    return app


async def close_rmq_connection(app):
    app["connection"].close()
    app["channel"].close()
    print("rmq connection and channel closed...")


def main():
    app = init_app()
    logging.basicConfig(level=logging.DEBUG)
    conf = config()
    web.run_app(app, port=conf["APP_PORT"])
