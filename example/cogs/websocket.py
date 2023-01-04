import bettersanic as bs
from sanic import response
import sanic

class Index(bs.Cog):
    def __init__(self, app: bs.BetterSanic) -> None:
        self.app = app
    
    @bs.websocket("/websocket")
    async def websocket(self, request: sanic.Request, ws: sanic.Websocket):
        async for msg in ws:
            await ws.send(msg)
            

def setup(app: bs.BetterSanic):
    app.add_cog(Index(app))