from app.views import (
    logs,
    users,
    auth
)


def setup_routes(app):
    # TODO: delete logs routes
    app.router.add_get('/api/_health', logs.health)
    app.router.add_get('/api/log/get', logs.get_logs_list)
    app.router.add_get('/api/log/get/{log_id}', logs.get_item)
    app.router.add_post('/api/log/create', logs.create_log)
    app.router.add_delete('/api/log/delete/{log_id}', logs.delete_item)
    app.router.add_patch('/api/log/patch/{log_id}', logs.patch_item)

    users.setup_user_routes(app)
    auth.setup_auth_routes(app)
