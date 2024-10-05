from aiohttp import web

from api import api_factory
from pkg.settings import Config, Redis

config = Config(
    DATABASE_URI="postgresql+asyncpg://postgres:postgres@localhost:5432/application",
    DEBUG=True,
    REDIS=Redis(REDIS_DB=0, REDIS_PORT=6379, REDIS_HOST="localhost"),
    APP_PORT=8080,
    RABBIT_URL="amqp://guest:guest@localhost/",
    APP_SECRET="secret_token_string",
)


web.run_app(api_factory(config), port=config.APP_PORT)
