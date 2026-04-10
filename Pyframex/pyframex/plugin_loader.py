import importlib
import pkgutil
from pyframex.plugins import Plugin


class PluginLoader:
    def __init__(self, package_name="plugin"):
        self.package_name = package_name

    def discover(self):
        plugins=[]
        package= importlib.import_module(self.package_name)

        for _, module_name,_ in pkgutil.iter_modules(package.__path__):
            module = importlib.import_module(f"{self.package_name}.{module_name}")

            for obj in module.__dict__.values():
                if ( isinstance(obj, type) and issubclass(obj, Plugin) and obj is not Plugin ):
                    plugins.append(obj())

        return plugins
    