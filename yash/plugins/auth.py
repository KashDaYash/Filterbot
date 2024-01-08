from yash import app
from yash.core.db import *
from config import *
from pyrogram import *
from pyrogram.types import *
import time


@app.on_message(filters.command("check") & filters.user(OWNER_ID))
async def chat_id_check(app, message):
    chat_id = message.chat.id
    if len(message.command) == 1:
        CHECKING = f"Please Provide Me In Correct Format /check <-chat id>"
        await message.reply(CHECKING, parse_mode=enums.ParseMode.MARKDOWN)
    else:
        try:
            n_id = int(message.text.split(None,1)[-1])
            group = await app.get_chat(n_id)
            uname = group.username
            await message.reply("You Giving Me @" + uname + " Chat ID")
        except Exception as e:
            await message.reply(str(e))
  
@app.on_message(filters.command("auth") & filters.private & filters.user(OWNER_ID))
async def auth_handle(app, message: Message):
    if len(message.command) == 1 or len(message.command) == 2:
        await message.reply("Please Provide Group ID And Time Period like /auth <Group ID> <Time>", parse_mode=enums.ParseMode.MARKDOWN)
        return 
    id = int(message.text.split(None,2)[1])
    group = await get_group(id)
    user_id = group["user_id"]
    user_name = group['user_name']
    verified = group["verified"]
    if verified == True:
        await message.reply(f"user id: {user_id}\nusername: @{user_name} group chat is already verified!")
        return 
    else:
        current = int(time.time())
        delta_sec = int(message.text.split(None, 2)[-1]) * 24 * 60 * 60
        new = current + delta_sec
        timestamp = time.strftime("%Y-%m-%d", time.localtime(new))
        await update_group(id, {"verified": True, "plan": new})
        await message.reply(f"user id: {user_id}\n username: @{user_name} group chat is verified!")
        await app.send_message(id, f"hey @{user_name} Purchase A Subscription For {timestamp} days ")
        return 
  
