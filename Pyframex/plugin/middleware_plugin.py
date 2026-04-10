from pyframex.plugins import Plugin
from plugin.Logging_middleware import LoggingMiddleware



class MiddlewarePlugin(Plugin):
    def register(self, app):
        logging_middleware = LoggingMiddleware()
        app.add_middleware(logging_middleware)