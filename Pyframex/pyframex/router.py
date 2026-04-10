from pyframex.exception import RouterNNotFound
from pyframex.middleware_manager import MiddlewareManager
from pyframex.context import Context
class Router:
    def __init__(self):
        self.routes={}
        self.middleware=MiddlewareManager()

    def route(self,path):
        def decorator(func):
            self.routes[path]=func
            return func
        return decorator
    
    async def dispatch(self,path):
        func=self.routes.get(path)
        if func is None:
            raise RouterNNotFound(f"No route found for {path}")
        Ctx=Context(path)
        handler =  self.routes[path]
        return  await self.middleware.execute(Ctx,  handler)