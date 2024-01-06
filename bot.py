import logging
from pyrogram import Client, idle 
from config import SESSION, API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL 
import asyncio 

# Initialize logging
FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
logging.basicConfig(
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
    format=FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S",
)
LOGGER = logging.getLogger(__name__)


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
        await YaaraOP.start()
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

if __name__ == "__main__":
    bot = Bot()
    bot.run()
    YaaraOP = UserBot()
    YaaraOP.run()
    idle()