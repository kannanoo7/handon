class Container:

    def __init__(self):
        self.providers={}

    def register(self, name, provider):
        self.providers[name] = provider
        if not hasattr(self, '_instances'):
            self._instances = {}

    def resolve(self, name):
        if not hasattr(self, '_instances'):
            self._instances = {}
        if name in self._instances:
            return self._instances[name]
        provider = self.providers.get(name)
        if provider is None:
            raise Exception(f"Provider for {name} not found")
        instance = provider()
        self._instances[name] = instance
        return instance