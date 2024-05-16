from app.views import admin, public


def setup_routes(app):
    public.setup_auth_routes(app)
    public.setup_apply_routes(app)


def setup_auth_routes(admin_app):
    admin.setup_admin_routes(admin_app)
    admin.setup_user_routes(admin_app)
    admin.setup_position_routes(admin_app)
    admin.setup_candidates_routes(admin_app)
