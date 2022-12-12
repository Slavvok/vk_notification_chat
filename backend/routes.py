from vk_notification_chatbot.main import index


def init_routes(app):
    app.router.add_post('/', index)
