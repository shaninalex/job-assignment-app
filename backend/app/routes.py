from app.views import (
    users,
    auth,
    admin
)


def setup_routes(app):
    admin.setup_admin_routes(app)
    auth.setup_auth_routes(app)
    users.setup_user_routes(app)
