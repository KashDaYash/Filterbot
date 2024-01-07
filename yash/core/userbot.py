import LOGGER 
from pyrogram import Client, idle 
from config import SESSION, API_ID, API_HASH, LOG_CHANNEL 
import asyncio 

class Userbot(Client):
    def __init__(self):
        super().__init__(
            "userbot_session",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=str(SESSION),
            no_updates=True,
            workers=3
        )

    async def start(self):
      try:
        await super().start()
        await super().send_message(LOG_CHANNEL, '@YaaraOP')
          # Start the User client
        LOGGER.info("UserBot Started ⚡")
      except Exception as e:
        LOGGER.exception("Error while starting userbot: %s", str(e))

    async def stop(self, *args):
      try:
        await super().stop()
        LOGGER.info("UserBot Stopped")
      except Exception as e:
        LOGGER.exception("Error while stopping userbot: %s", str(e))
