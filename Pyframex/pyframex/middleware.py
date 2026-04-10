class Middleware:
    async def process(self,Context,next_call):
        raise NotImplementedError("Middleware must implement process method")
