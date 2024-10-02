from .routes_auth import setup_auth_routes
from .routes_jobs import setup_jobs_routes


def setup_public_routes(app):
    setup_auth_routes(app)
    setup_jobs_routes(app)
