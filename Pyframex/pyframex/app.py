from pyframex.config import Config
from pyframex.container import Container
from pyframex.hooks import Hooks
from pyframex.logger import get_logger
from pyframex.exception import PyframexError
from pyframex.plugin_loader import PluginLoader

class  App:
    def __init__(self,container:Container,config:Config):
        self.logger=get_logger()
        self.config=config
        self.container=container
        self.hooks=Hooks()
        self.plugins=[]

    def register_plugin(self, plugin):
        plugin.register(self)
        self.plugins.append(plugin)

    def add_middleware(self, middleware):
        router=self.container.resolve("router")
        router.middleware.add(middleware)

    def load_plugins(self):
        loader =PluginLoader()
        for plugin in loader.discover():
            self.register_plugin(plugin)

    def run(self):
        try:
            self.hooks.emit("before_start")
            self.logger.info("App is starting")
            print("App is running")
        except PyframexError as e:
            self.logger.error(f"Error occurred: {e}" )
            raise
        # self.hooks.emit("after_start")