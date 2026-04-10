from pyframex.middleware import Middleware
from pyframex.plugins import Plugin


class LoggingMiddleware(Middleware):
      async def   process (self,Context,next_call):
        print(f"LoggingMiddleware: Handling request for {Context.path}")
        result =  next_call()
        if hasattr(result, "__await__"):
            result = await result
        print(f'''LoggingMiddleware: Finished handling request for {Context.path} 
              with status {Context.status_code}''')
        return   result
     



