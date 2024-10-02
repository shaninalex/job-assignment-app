from aiohttp import web

from api import init_app
from api.settings import config
from pkg.database import utils

app = init_app()
conf = config()


if __name__ == "__main__":
    utils.check_migrations()
    web.run_app(app, port=conf["APP_PORT"])
