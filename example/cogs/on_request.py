import bettersanic as bs
import sanic
from typing import Any


class OnRequest(bs.Cog):
    def __init__(self, app: bs.BetterSanic[sanic.Config, Any]) -> None:
        self.app = app

    @bs.middleware("request")
    async def index(self, request: sanic.Request):
        print("request middleware ran")


def setup(app: bs.BetterSanic[sanic.Config, Any]):
    app.add_cog(OnRequest(app))
