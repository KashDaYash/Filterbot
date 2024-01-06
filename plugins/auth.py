from bot import Client
from db import *
from config import *
from pyrogram import *
from pyrogram.types import *
import time





@Client.on_message(filters.command("check") & filters.user(OWNER_ID))
async def chat_id_check(bot: Client, m):
    chat_id = m.chat.id
    if len(m.command) == 1:
        CHECKING = "Please Provide Me In Correct Format /check -chat id"
        await m.reply(CHECKING)
    else:
        n_id = int(m.text.split(None,1)[-1])
        group = await bot.get_chat(n_id)
        uname = group.username
        await m.reply("You Giving Me @" + uname + " Chat ID")
  
@Client.on_message(filters.command("auth") & filters.private & filters.user(OWNER_ID))
async def auth_handle(bot: Client, m: Message):
    if len(m.command) == 1 or len(m.command) == 2:
        await m.reply("Please Provide Group ID And Time Period like /auth <Group ID> <Time>", parse_mode=enums.ParseMode.MARKDOWN)
        return 
    id = int(m.text.split(None,2)[1])
    group = await get_group(id)
    user_id = group["user_id"]
    user_name = group['user_name']
    verified = group["verified"]
    if verified == True:
        await m.reply(f"user id: {user_id}\nusername: @{user_name} group chat is already verified!")
        return 
    else:
        current = int(time.time())
        delta_sec = int(m.text.split(None, 2)[-1]) * 24 * 60 * 60
        new = current + delta_sec
        timestamp = time.strftime("%Y-%m-%d", time.localtime(new))
        await update_group(id, {"verified": True, "plan": new})
        await m.reply(f"user id: {user_id}\n username: @{user_name} group chat is verified!")
        await bot.send_message(id, f"hey @{user_name} Purchase A Subscription For {timestamp} days ")
        return 
  
