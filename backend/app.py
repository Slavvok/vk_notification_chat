from main import index
from aiohttp import web

# def init_app() -> web.Application:
#     app = web.Application()
#     app.router.add_post('/', index)
#     return app


app = web.Application()
app.router.add_post('/', index)

web.run_app(app)
