from aiohttp import web

from api import init_app
from pkg.settings import CONFIG

web.run_app(init_app(), port=CONFIG.APP_PORT)
