import bettersanic as bs
import asyncio
import sanic
from typing import Any


class MainProcessStop(bs.Cog):
    def __init__(self, app: bs.BetterSanic[sanic.Config, Any]) -> None:
        self.app = app

    @bs.listener("main_process_stop")
    async def main_process_stop(
        self, app: bs.BetterSanic[sanic.Config, Any], loop: asyncio.AbstractEventLoop
    ):
        print("The app has shut down.")


def setup(app: bs.BetterSanic[sanic.Config, Any]):
    app.add_cog(MainProcessStop(app))
