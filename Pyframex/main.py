import asyncio
from pyframex import router
from pyframex.app import App
from pyframex.config import Config
from plugin.HelloPlugin import  HelloPlugin
from pyframex.container import Container
from pyframex.router import Router
from  plugin.middleware_plugin import MiddlewarePlugin
from pyframex.asgi import ASGIAdapter  
from pyframex.response import Response

def before_start():
    print("Before start hook called")
def after_start():
    print("After start hook called")


 
container =Container()
container.register("router",Router)
config = Config(debug=True,app_name="Pyframex")

app=App(container,config)

app.load_plugins()  #  ----> auto_discovery 

# app.hooks.register("before_start", before_start)
# app.hooks.register("after_start", after_start)
# app.register_plugin(HelloPlugin())
# app.register_plugin(MiddlewarePlugin())

router=container.resolve("router")
# @router.route("/")
# async def home():
#     return "Hello, Pyframex!"

# asgi_app = ASGIAdapter(router)


# @router.route("/sync")
# def hello(ctx):
#     ctx.body="sync response" 
#     return ctx.body

@router.route("/Async")
async def async_hello(ctx):
    # ctx.body="async response"
    return Response.text("async response")

# router.dispatch("/sync")

import asyncio
async def main():
    await router.dispatch("/Async")

asyncio.run(main())
app.run()
# config = Config(debug=True)
# app=App(config)

# HelloPlugin().register(app)
# app.run()

