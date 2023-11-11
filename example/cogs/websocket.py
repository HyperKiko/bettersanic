import bettersanic as bs
import sanic

class Websocket(bs.Cog):
    def __init__(self, app: bs.BetterSanic) -> None:
        self.app = app
    
    @bs.websocket("/websocket")
    async def websocket(self, request: sanic.Request, ws: sanic.Websocket):
        async for msg in ws:
            if msg is None: continue
            await ws.send(msg)
            

def setup(app: bs.BetterSanic):
    app.add_cog(Websocket(app))