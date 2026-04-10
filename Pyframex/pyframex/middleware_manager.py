import inspect
from pyframex.utils import is_awaitable

class MiddlewareManager:
    def __init__(self):
        self.middlewares=[]

    def add(self,middleware):
        self.middlewares.append(middleware)

    async def execute(self,Context,handler):
        async def build_chain(index):
            if index == len(self.middlewares):
                result=handler(Context)
                if is_awaitable(result):
                    return await result
                return result
            
            middleware=self.middlewares[index]
            result= middleware.process(Context, lambda:build_chain(index+1))
            if is_awaitable(result):
                return await result
            return result
        return await build_chain(0)
        # chain=build_chain(0)
        # return  chain()