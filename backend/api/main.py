import logging

import pika
from aiohttp import web
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from api.middlewares.utils import setup_middlewares
from api.routes import public, company
from api.settings import config
from database.utils import database_url
from pkg import rabbitmq


def setup_routes(app):
    public.setup_auth_routes(app)
    company.setup_company_routes(app)


def init_app():
    app = web.Application()
    app["config"] = config()
    session = async_sessionmaker(
        create_async_engine(database_url(), echo=False), expire_on_commit=False
    )
    app["session"] = session()

    try:
        # TODO: use os.getenv credential and host variables
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                "localhost", credentials=pika.PlainCredentials("guest", "guest")
            )
        )
        app["mq"] = connection
    except Exception as e:
        logging.error(f"Failed to connect to RabbitMQ: {e}")
        app["mq"] = None


    setup_middlewares(app)
    setup_routes(app)

    app.on_startup.append(rabbitmq.start_background_tasks)
    app.on_shutdown.append(rabbitmq.cancel_background_tasks)
    app.on_shutdown.append(rabbitmq.close_rmq_connection)

    logging.info("Main app initialized")
    return app

