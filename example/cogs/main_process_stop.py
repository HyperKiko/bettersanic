import bettersanic as bs
import asyncio

class MainProcessStop(Exception):
    pass

class MainProcessStop(bs.Cog):
    def __init__(self, app: bs.BetterSanic) -> None:
        self.app = app
    
    @bs.listener("main_process_stop")
    async def main_process_stop(self, app: bs.BetterSanic, loop: asyncio.AbstractEventLoop):
        raise MainProcessStop("The App has been Terminated.")

def setup(app: bs.BetterSanic):
    app.add_cog(MainProcessStop(app))
