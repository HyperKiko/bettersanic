import bettersanic as bs
from sanic import response
from sanic import exceptions
import sanic
from typing import Any


class NotFound(bs.Cog):
    def __init__(self, app: bs.BetterSanic[sanic.Config, Any]) -> None:
        self.app = app

    @bs.exception(exceptions.NotFound)
    async def index(self, request: sanic.Request, exception: BaseException):
        return response.text(f'The route "{request.path}" was not found.')


def setup(app: bs.BetterSanic[sanic.Config, Any]):
    app.add_cog(NotFound(app))
