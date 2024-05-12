from app.views import (
    users,
    auth,
    admin
)


def setup_routes(app):
    auth.setup_auth_routes(app)


def setup_auth_routes(admin_app):
    admin.setup_admin_routes(admin_app)
    users.setup_user_routes(admin_app)
