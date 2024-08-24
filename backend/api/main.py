import logging

import pika
from aiohttp import web
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from api.middlewares.utils import setup_middlewares
from api.routes import public
from api.settings import config
from database.utils import database_url


def setup_routes(app):
    public.setup_auth_routes(app)


def init_app():
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

    app["mq"] = connection
    app.on_shutdown.append(close_rmq_connection)

    setup_middlewares(app)
    setup_routes(app)

    logging.info("Main app initialized")
    return app


async def close_rmq_connection(app):
    app["mq"].close()
    print("rmq connection and channel closed...")


# DeprecationWarning
# this method is deprecated since we need to run application in a different ways ( live/dev )
# def main():
#     app = init_app()
#     logging.basicConfig(level=logging.DEBUG)
#     conf = config()
#     web.run_app(app, port=conf["APP_PORT"])
