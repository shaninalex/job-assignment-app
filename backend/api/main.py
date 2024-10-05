import logging

from aiohttp import web
from aiohttp_cache import setup_cache, RedisConfig

from api.middlewares.error import error_middleware
from api.routes import public, company, utils
from pkg.container import Container
from pkg.database import db_session_middleware
from pkg.settings import Config


def setup_routes(app):
    utils.setup_utils_routes(app)
    public.setup_public_routes(app)
    company.setup_company_routes(app)


async def api_factory(config: Config):
    app = web.Application()
    container = Container()
    app.container = container
    await container.event_service().connect()

    # TODO: https://docs.aiohttp.org/en/stable/web_advanced.html#application-s-config
    app["config"] = config

    setup_cache(
        app,
        cache_type="redis",
        backend_config=RedisConfig(
            host=config.REDIS.REDIS_HOST,
            port=config.REDIS.REDIS_PORT,
            db=config.REDIS.REDIS_DB,
        ),
    )

    app.middlewares.append(error_middleware)
    app.middlewares.append(db_session_middleware)

    setup_routes(app)

    logging.info("App initialized")
    return app
