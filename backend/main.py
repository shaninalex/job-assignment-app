from aiohttp import web
from api import init_app
from api.settings import config
from database.utils import check_migrations

app = init_app()
conf = config()

if __name__ == "__main__":
    check_migrations()
    web.run_app(app, port=conf["APP_PORT"])
