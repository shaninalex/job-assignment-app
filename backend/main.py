from aiohttp import web

from api import api_factory
from pkg.settings import CONFIG

web.run_app(api_factory(CONFIG), port=CONFIG.APP_PORT)
