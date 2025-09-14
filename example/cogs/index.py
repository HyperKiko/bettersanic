import bettersanic as bs
from sanic import response
import sanic
from typing import Any


class Index(bs.Cog):
    def __init__(self, app: bs.BetterSanic[sanic.Config, Any]) -> None:
        self.app = app

    @bs.route("/")
    async def index(self, request: sanic.Request):
        return response.text("Hello, World!")


def setup(app: bs.BetterSanic[sanic.Config, Any]):
    app.add_cog(Index(app))
