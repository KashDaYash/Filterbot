from yash import LOGGER 
from pyrogram import Client, idle 
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL 
import asyncio 



class Bot(Client):
    def __init__(self):
        super().__init__(
            "bot_session",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins={"root": "plugins"},
            workers=5
        )

    async def start(self):
      try:
        await super().start()
        await super().send_message(LOG_CHANNEL, "STARTED 💥 ")
          # Start the User client
        LOGGER.info("Bot Started ⚡")
      except Exception as e:
        LOGGER.exception("Error while starting bot: %s", str(e))

    async def stop(self, *args):
      try:
        await super().stop()
        LOGGER.info("Bot Stopped")
      except Exception as e:
        LOGGER.exception("Error while stopping bot: %s", str(e))


