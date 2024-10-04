import logging

from aiohttp import web
from aiohttp_cache import setup_cache, RedisConfig

from api.middlewares.utils import error_middleware
from api.routes import public, company
from pkg.container import Container
from pkg.database import db_session_middleware
from pkg.settings import CONFIG


def setup_routes(app):
    public.setup_public_routes(app)
    company.setup_company_routes(app)


async def init_app():
    app = web.Application()
    container = Container()
    app.container = container
    await container.event_service().connect()

    app["config"] = CONFIG

    setup_cache(
        app,
        cache_type="redis",
        backend_config=RedisConfig(
            host=CONFIG.REDIS.REDIS_HOST,
            port=CONFIG.REDIS.REDIS_PORT,
            db=CONFIG.REDIS.REDIS_DB,
        ),
    )

    app.middlewares.append(db_session_middleware)
    app.middlewares.append(error_middleware)

    setup_routes(app)

    logging.info("Main app initialized")
    return app
