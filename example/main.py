from typing import Any
from bettersanic import BetterSanic
import os
from sanic import Config

app = BetterSanic[Config, Any]("BetterSanic-Example")

for cog in os.listdir("cogs"):
    if cog.endswith(".py"):
        app.load_extension(f"cogs.{cog[:-3]}")

if __name__ == "__main__":
    app.run()  # type: ignore # not my fault
