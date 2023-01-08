from main import update_order_status, main_page


def init_routes(app):
    app.router.add_get('/get', main_page)
    app.router.add_post('/', update_order_status)
