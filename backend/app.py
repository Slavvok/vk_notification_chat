from aiohttp import web
from routes import init_routes

# def init_app() -> web.Application:
#     app = web.Application()
#     app.router.add_post('/', index)
#     return app


app = web.Application()
init_routes(app)

web.run_app(app)
