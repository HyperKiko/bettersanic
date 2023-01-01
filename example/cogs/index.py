import bettersanic as bs
from sanic import response
import sanic

class Index(bs.Cog):
    def __init__(self, app: bs.BetterSanic) -> None:
        self.app = app
    
    @bs.route("/")
    async def index(self, request: sanic.Request):
        return response.text("Hello, World!")

def setup(app: bs.BetterSanic):
    app.add_cog(Index(app))