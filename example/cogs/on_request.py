import bettersanic as bs
import sanic

class Index(bs.Cog):
    def __init__(self, app: bs.BetterSanic) -> None:
        self.app = app
    
    @bs.middleware("request")
    async def index(self, request: sanic.Request):
        print("request middleware ran")

def setup(app: bs.BetterSanic):
    app.add_cog(Index(app))