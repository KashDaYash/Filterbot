from yash import app
from yash.core.db import *
from config import OWNER_ID
from pyrogram import *
from pyrogram.types import *
import time 
import os
from yash.logging import LOGGER 

@app.on_message(filters.command("log"))
async def logo_handle_bot(client: Client, message: Message):
    chat_id = message.chat.id
    await message.reply_document(document="log.txt")
    return 
@app.on_message(filters.command("info"))
async def info_handle(app: Client, message: Message):
    chat = message.chat
    if chat.type == enums.ChatType.PRIVATE:
        return await message.reply("Please Use In Group Chat")
    msg = await message.reply("checking your subscription⌛")
    dexa = await get_group(chat.id)
    plan = dexa["plan"]
    await asyncio.sleep(1)
    name = message.from_user.mention
    if not plan:
        BUTTON = InlineKeyboardMarkup([[
            InlineKeyboardButton("Buy A Plan", user_id=OWNER_ID)]])
        await msg.edit_reply_markup(text=f"Hey {name} You haven't a Subscription ",reply_markup=BUTTON)
    else:
        await asyncio.sleep(1)
        stamp = time.strftime("%Y-%m-%d", time.localtime(int(plan)))
        await msg.edit(f"Your Subscription till {stamp} ⏳")
  
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
        