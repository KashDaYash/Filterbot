from bot import Bot
from pyrogram import idle
import asyncio 

bot = Bot()

async def main():
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
