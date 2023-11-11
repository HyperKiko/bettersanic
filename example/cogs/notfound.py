import bettersanic as bs
from sanic import response
from sanic import exceptions
import sanic

class NotFound(bs.Cog):
    def __init__(self, app: bs.BetterSanic) -> None:
        self.app = app
    
    @bs.exception(exceptions.NotFound)
    async def index(self, request: sanic.Request, exception: BaseException):
        return response.text(f"The route \"{request.path}\" was not found.")

def setup(app: bs.BetterSanic):
    app.add_cog(NotFound(app))