from yash import app
from yash.core.db import *
from config import OWNER_ID
from pyrogram import *
from pyrogram.types import *
import time 
import os
from yash.logging import LOGGER 

@app.on_message(filters.command("info"))
async def info_handle(_, m):
    chat_id = m.chat.id
    if m.chat.type == enums.ChatType.PRIVATE:
        return await m.reply("Please Use In Group Chat")
    await m.reply("checking your subscription⌛")
    dexa = await get_group(chat_id)
    plan = dexa["plan"]
    await asyncio.sleep(1)
    await m.edit("founded subscription⌛")
    name = m.from_user.mention
    if plan:
        await asyncio.sleep(1)
        stamp = time.strftime("%Y-%m-%d", time.localtime(int(plan)))
        await m.edit(f"Your Subscription till {stamp} ⏳")
        return 
    
    else:
        BUTTON = InlineKeyboardMarkup([[
            InlineKeyboardButton("Buy A Plan", user_id=OWNER_ID)]])
        await m.edit_reply_markup(text=f"Hey {name} You haven't a Subscription ",reply_markup=BUTTON)
  
@app.on_message(filters.command('leave') & filters.private &  filters.chat(OWNER_ID))
async def leave_a_chat(app, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        chat = chat
    try:
        buttons = [[
            InlineKeyboardButton('𝚂𝚄𝙿𝙿𝙾𝚁𝚃', url=f'https://t.me/YaaraOP')
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await app.send_message(
            chat_id=chat,
            text='<b>Hello Friends, \nMy admin has told me to leave from group so i go! If you wanna add me again contact my support group.</b>',
            reply_markup=reply_markup,
        )

        await app.leave_chat(chat)
        await message.reply(f"left the chat `{chat}`")
    except Exception as e:
        await message.reply(f'Error - {e}')
        