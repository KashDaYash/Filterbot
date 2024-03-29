from config import *
from yash.core.db import *
from pyrogram import *
from pyrogram.types import *
from yash import app

@app.on_message(filters.group & filters.command("forcesub"))
async def f_sub_cmd(app, message):
    m=await message.reply("Please wait..")
    try:
       group     = await get_group(message.chat.id)
       user_id   = group["user_id"] 
       user_name = group["user_name"]
       verified  = group["verified"]
    except :
       return await app.leave_chat(message.chat.id)  
    if message.from_user.id!=user_id:
       return await m.edit(f"Only {user_name} can use this command 😁")
    if bool(verified)==False:
       return await m.edit(f"You Didn't Purchase any plan!\n Contact To My Owner @{OWNER}")    
    try:
       f_sub = int(message.command[-1])
    except:
       return await m.edit("❌ Incorrect format!\nUse `/forcesub ChannelID`")       
    try:
       chat   = await app.get_chat(f_sub)
       group  = await app.get_chat(message.chat.id)
       c_link = chat.invite_link
       g_link = group.invite_link       
    except Exception as e:
       text = f"❌ Error: `{str(e)}`\n\nMake sure I'm admin in that channel & this group with all permissions"
       return await m.edit(text)
    await update_group(message.chat.id, {"f_sub":f_sub})
    await m.edit(f"✅ Successfully Attached ForceSub to [{chat.title}]({c_link})!", disable_web_page_preview=True)
    text = f"#NewFsub\n\nUser: {message.from_user.mention}\nGroup: [{group.title}]({g_link})\nChannel: [{chat.title}]({c_link})"
    await app.send_message(chat_id=LOG_CHANNEL, text=text)

@app.on_message(filters.group & filters.command("nofsub"))
async def nf_sub_cmd(app, message):
    m=await message.reply("Disattaching..")
    try:
       group     = await get_group(message.chat.id)
       user_id   = group["user_id"] 
       user_name = group["user_name"]
       verified  = group["verified"]
       f_sub     = group["f_sub"]
    except :
       return await app.leave_chat(message.chat.id)  
    if message.from_user.id!=user_id:
       return await m.edit(f"Only {user_name} can use this command 😁")
    if bool(verified)==False:
       return await m.edit("This chat is not verified!\nuse /verify")        
    if bool(f_sub)==False:
       return await m.edit("This chat is currently don't have any FSub\nuse /forcesub")        
    try:
       chat   = await app.get_chat(f_sub)
       group  = await app.get_chat(message.chat.id)
       c_link = chat.invite_link
       g_link = group.invite_link       
    except Exception as e:
       text = f"❌ Error: `{str(e)}`\n\nMake sure I'm admin in that channel & this group with all permissions"
       return await m.edit(text)
    await update_group(message.chat.id, {"f_sub":False})
    await m.edit(f"✅ Successfully removed FSub from [{chat.title}]({c_link})!", disable_web_page_preview=True)
    text = f"#RemoveFsub\n\nUser: {message.from_user.mention}\nGroup: [{group.title}]({g_link})\nChannel: [{chat.title}]({c_link})"
    await app.send_message(chat_id=LOG_CHANNEL, text=text)

       
@app.on_callback_query(filters.regex(r"^checksub"))
async def f_sub_callback(app, update):
    user_id = int(update.data.split("_")[-1])
    group   = await get_group(update.message.chat.id)
    f_sub   = group["f_sub"]
    admin   = group["user_id"]

    if update.from_user.id!=user_id:
       return await update.answer("That's not for you 😂", show_alert=True)
    try:
       await app.get_chat_member(f_sub, user_id)          
    except UserNotParticipant:
       await update.answer("I like your smartness..\nBut don't be over smart 🤭", show_alert=True) # @subinps 😁
    except:       
       await app.restrict_chat_member(chat_id=update.message.chat.id, 
                                      user_id=user_id,
                                      permissions=ChatPermissions(can_send_messages=True,
                                                                  can_send_media_messages=True,
                                                                  can_send_other_messages=True))
       await update.message.delete()
    else:
       await app.restrict_chat_member(chat_id=update.message.chat.id, 
                                      user_id=user_id,
                                      permissions=ChatPermissions(can_send_messages=True,
                                                                  can_send_media_messages=True,
                                                                  can_send_other_messages=True))
       await update.message.delete()