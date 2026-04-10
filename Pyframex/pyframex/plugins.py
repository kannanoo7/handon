class Plugin:
    def register(self,app):
        raise NotImplementedError("Plugin must implement register method")