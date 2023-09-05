import logging
import concurrent.futures
from pyrogram import Client
from config import *
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

YaaraOP = Client(name="user_session", session_string=SESSION)
# Initialize the Pyrogram clients
def __init__(self):
  super().__init__(
    "bot_session",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins={"root": "plugins"}
  )


        # Define the executor
  executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)  # Adjust max_workers as needed

async def start_bot(self):
  try:
    await super().start()
    await YaaraOP.start()
    await YaaraOP.send_message("me", 'chtuiteg')  # Start the User client
    LOGGER.info("Bot Started ⚡")
  except Exception as e:
    LOGGER.exception("Error while starting bot: %s", str(e))

async def stop_bot(self, *args):
  try:
    await super().stop()
    await YaaraOP.stop()  # Stop the User client
    LOGGER.info("Bot Stopped")
  except Exception as e:
    LOGGER.exception("Error while stopping bot: %s", str(e))

def run_in_executor(fn, *args, **kwargs):
    return executor.submit(fn, *args, **kwargs)

  
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_bot())
    try:
        # Your bot's logic can go here
        pass
    except KeyboardInterrupt:
        pass
    finally:
        asyncio.get_event_loop().run_until_complete(stop_bot())
