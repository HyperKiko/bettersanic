from bettersanic import BetterSanic
import os

app = BetterSanic("BetterSanic-Example")

for cog in os.listdir("cogs"):
    if cog.endswith(".py"):
        app.load_extension(f"cogs.{cog[:-3]}")

if __name__ == "__main__":
    app.run() # type: ignore # not my fault