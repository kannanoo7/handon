from pyframex.plugins import  Plugin


class HelloPlugin(Plugin):
    def register(self, app):
        if app.config.get("debug"):
            print("HelloPlugin registered in debug mode")
        app.hooks.register("before_start", self.say_hello)

    def say_hello(self):
        print("Hello from HelloPlugin!")
