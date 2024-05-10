from . import views


def setup_routes(app):
    app.router.add_get('/api/_health', views.health)
    app.router.add_get('/api/log/get', views.get_logs_list)
    app.router.add_get('/api/log/get/{log_id}', views.get_item)
    app.router.add_post('/api/log/create', views.create_log)
    app.router.add_delete('/api/log/delete/{log_id}', views.delete_item)
    app.router.add_patch('/api/log/patch/{log_id}', views.patch_item)


