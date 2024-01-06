from config import LOG_CHANNEL, OWNER_ID 
from db import *
from asyncio import sleep
from pyrogram import *
from bot import app
from pyrogram.errors import *


@app.on_message(filters.group & filters.new_chat_members)
async def new_group(app, message):
    bot_id = (await app.get_me()).id
    member = [u.id for u in message.new_chat_members]        
    if bot_id in member:
       await add_group(group_id=message.chat.id, 
                       group_name=message.chat.title,
                       user_name=message.from_user.username, 
                       user_id=message.from_user.id, 
                       channels=[],
                       f_sub=False,
                       verified=False,plan="",auto_del=False)
       m=await message.reply(f"Thanks for adding me in {message.chat.title} ✨")
       num_of_members = await app.get_chat_members_count(message.chat.id) # get the number of members in the group
       text=f"#NewGroup\n\nGroup: {message.chat.title}\nGroupID: `{message.chat.id}`\nAddedBy: {message.from_user.mention}\nUserID: `{message.from_user.id}`\nNumber of Members: {num_of_members}"
       try:
         await app.send_message(chat_id=LOG_CHANNEL, text=text)
         await sleep(60)
       except Exception as e:
         omk =await app.send_message(OWNER_ID,e)
         await omk.delete()
         await app.send_message(OWNER_ID, text=text)
       await m.delete()