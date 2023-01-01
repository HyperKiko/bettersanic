import bettersanic as bs
from sanic import response
import asyncio

class MainProcessStop(bs.Cog):
    def __init__(self, app: bs.BetterSanic) -> None:
        self.app = app
    
    @bs.listener("main_process_stop")
    async def main_process_stop(self, app: bs.BetterSanic, loop: asyncio.AbstractEventLoop):
        print("The app has shut down.")

def setup(app: bs.BetterSanic):
    app.add_cog(MainProcessStop(app))