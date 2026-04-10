from pyframex.context import Context
from pyframex.exception import RouterNNotFound


class ASGIAdapter:
    def __init__(self,router):
        self.router=router

    async def __call__(self,scope,receive,send):
        if scope["type"]!='http':
            return  
        path=scope["path"]
        context_=Context(path)
        try:
            result= await self.router.dispatch(path)
            context_.body=result
        except RouterNNotFound :
            context_.status=404
            context_.body="Not Found"
        await send({
             "type":"http.response.start",
                "status":context_.status,
                "headers":[(b"content-type",b"text/plain")]
        })

        await send({
            "type":"http.response.body",
            "body" :(context_.body).encode()})
        