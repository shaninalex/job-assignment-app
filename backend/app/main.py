import logging

from aiohttp import web

from app.db import db_context
from app.middlewares.auth import auth_middleware
from app.middlewares.utils import setup_middlewares
from app.routes import setup_auth_routes, setup_routes
from app.settings import config


def init_admin_app() -> web.Application:
    admin = web.Application()
    admin["config"] = config()
    admin.cleanup_ctx.append(db_context)
    admin.middlewares.append(auth_middleware)
    setup_auth_routes(admin)
    logging.info("Admin app initialized")
    return admin


async def init_app():
    app = web.Application()

    app["config"] = config()

    # create db connection on startup, shutdown on exit
    app.cleanup_ctx.append(db_context)

    # setup views and routes
    setup_routes(app)
    setup_middlewares(app)
    admin_app = init_admin_app()
    app.add_subapp("/api/admin/", admin_app)
    logging.info("Main app initialized")
    return app


def main():
    app = init_app()
    logging.basicConfig(level=logging.DEBUG)
    conf = config()
    web.run_app(app, host=conf["APP_HOST"], port=conf["APP_PORT"])
