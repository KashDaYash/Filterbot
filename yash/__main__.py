import asyncio
import importlib

from pyrogram import idle

import config
from yash import LOGGER, app, yk
from yash.plugins import ALL_MODULES


async def init():
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("yash.plugins." + all_module)
    LOGGER("yash.plugins").info("Successfully Imported Modules...")
    await app.start()
    await yk.start()
    await idle()
    await app.stop()
    await yk.stop()
    LOGGER("yash").info("Stopping Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
