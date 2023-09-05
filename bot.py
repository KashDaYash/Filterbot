import logging
import concurrent.futures
from pyrogram import Client
from config import SESSION, API_ID, API_HASH, BOT_TOKEN
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

# Initialize clients
YaaraOP = Client(name="user_session", session_string=SESSION)


class Bot(Client):
    def __init__(self):
        super().__init__(
            "bot_session",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins={"root": "plugins"}
        )
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)  # Adjust max_workers as needed 

    async def start(self):
      try:
        await super().start()
        await YaaraOP.start()
        await YaaraOP.send_message("me", 'chtuiteg')  # Start the User client
        LOGGER.info("Bot Started ⚡")
      except Exception as e:
        LOGGER.exception("Error while starting bot: %s", str(e))

    async def stop(self, *args):
      try:
        await super().stop()
        await YaaraOP.stop()  # Stop the User client
        LOGGER.info("Bot Stopped")
      except Exception as e:
        LOGGER.exception("Error while stopping bot: %s", str(e))

    def run_in_executor(self, fn, *args, **kwargs):
      return self.executor.submit(fn, *args, **kwargs)
async def main():
  await Bot().run()
  idle()
  
  
if __name__ == "__main__":
  asyncio.get_event_loop().run_until_complete(main())
  try:
    # Your bot's logic can go here
    pass
  except KeyboardInterrupt:
    pass
    